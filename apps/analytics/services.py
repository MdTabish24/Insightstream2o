import statistics
import logging
from datetime import datetime, timezone
from core.clients.youtube import youtube_client
from core.clients.gemini import gemini_client
from core.exceptions import YouTubeAPIError, AIServiceUnavailable

logger = logging.getLogger(__name__)

class AnalyticsService:
    def calculate_smart_score(self, views: float, velocity: float, engagement: float, max_views: float, max_velocity: float, max_engagement: float) -> float:
        norm_views = views / max_views if max_views > 0 else 0
        norm_velocity = velocity / max_velocity if max_velocity > 0 else 0
        norm_engagement = engagement / max_engagement if max_engagement > 0 else 0
        return (0.5 * norm_views) + (0.3 * norm_velocity) + (0.2 * norm_engagement)
    
    def detect_outliers(self, channel_id: str) -> dict:
        """Detect outlier videos using IQR method and SmartScore."""
        try:
            # Get channel videos
            videos = youtube_client.get_channel_videos(channel_id, max_results=50)
            
            if len(videos) < 4:
                return {
                    'channel_id': channel_id,
                    'error': 'Not enough videos for outlier detection (minimum 4 required)',
                    'high_outliers': [],
                    'low_outliers': []
                }
            
            # Calculate SmartScores for all videos
            video_scores = []
            for video in videos:
                # Calculate velocity (views per day)
                publish_date = datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - publish_date).days
                days_old = max(1, days_old)
                velocity = video['views'] / days_old
                
                # Calculate engagement rate
                total_engagement = video['likes'] + video['comments']
                engagement = (total_engagement / video['views']) if video['views'] > 0 else 0
                
                video_scores.append({
                    'video': video,
                    'views': video['views'],
                    'velocity': velocity,
                    'engagement': engagement
                })
            
            # Find max values for normalization
            max_views = max(v['views'] for v in video_scores)
            max_velocity = max(v['velocity'] for v in video_scores)
            max_engagement = max(v['engagement'] for v in video_scores)
            
            # Calculate SmartScore for each video
            for item in video_scores:
                smart_score = self.calculate_smart_score(
                    item['views'], item['velocity'], item['engagement'],
                    max_views, max_velocity, max_engagement
                )
                item['smart_score'] = smart_score
            
            # Calculate IQR
            scores = [item['smart_score'] for item in video_scores]
            scores.sort()
            
            q1 = statistics.quantiles(scores, n=4)[0]
            q3 = statistics.quantiles(scores, n=4)[2]
            iqr = q3 - q1
            
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            
            # Identify outliers
            high_outliers = []
            low_outliers = []
            
            for item in video_scores:
                video = item['video']
                score = item['smart_score']
                
                outlier_data = {
                    'video_id': video['id'],
                    'title': video['title'],
                    'thumbnail_url': video['thumbnail_url'],
                    'views': video['views'],
                    'likes': video['likes'],
                    'comments': video['comments'],
                    'publish_date': video['publish_date'],
                    'views_per_day': round(item['velocity'], 2),
                    'engagement_rate': round(item['engagement'] * 100, 2),
                    'smart_score': round(score, 4)
                }
                
                if score > upper_bound:
                    high_outliers.append(outlier_data)
                elif score < lower_bound:
                    low_outliers.append(outlier_data)
            
            # Sort by smart_score
            high_outliers.sort(key=lambda x: x['smart_score'], reverse=True)
            low_outliers.sort(key=lambda x: x['smart_score'])
            
            return {
                'channel_id': channel_id,
                'total_videos': len(videos),
                'high_outliers': high_outliers,
                'low_outliers': low_outliers,
                'statistics': {
                    'q1': round(q1, 4),
                    'q3': round(q3, 4),
                    'iqr': round(iqr, 4),
                    'lower_bound': round(lower_bound, 4),
                    'upper_bound': round(upper_bound, 4)
                }
            }
        except YouTubeAPIError as e:
            logger.error(f'YouTube API error in outlier detection: {str(e)}')
            return {'channel_id': channel_id, 'error': str(e), 'high_outliers': [], 'low_outliers': []}
    
    def analyze_upload_streak(self, channel_id: str) -> dict:
        """Analyze upload consistency and calculate algorithm score."""
        try:
            # Get last 50 videos
            videos = youtube_client.get_channel_videos(channel_id, max_results=50)
            
            if not videos:
                return {
                    'channel_id': channel_id,
                    'error': 'No videos found for channel',
                    'algorithm_score': 0
                }
            
            # Separate Shorts and regular videos
            shorts = []
            regular = []
            
            for video in videos:
                duration = video.get('duration', '')
                # Parse ISO 8601 duration (e.g., PT1M30S)
                is_short = self._is_short_video(duration)
                
                if is_short:
                    shorts.append(video)
                else:
                    regular.append(video)
            
            # Calculate upload consistency
            upload_dates = []
            for video in videos:
                publish_date = datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00'))
                upload_dates.append(publish_date)
            
            upload_dates.sort()
            
            # Calculate gaps between uploads
            gaps = []
            for i in range(1, len(upload_dates)):
                gap = (upload_dates[i] - upload_dates[i-1]).days
                gaps.append(gap)
            
            # Calculate consistency metrics
            avg_gap = statistics.mean(gaps) if gaps else 0
            consistency = 100 - min(statistics.stdev(gaps) if len(gaps) > 1 else 0, 100)
            
            # Calculate view performance
            avg_views = statistics.mean([v['views'] for v in videos]) if videos else 0
            
            # Calculate engagement
            total_engagement = sum(v['likes'] + v['comments'] for v in videos)
            total_views = sum(v['views'] for v in videos)
            engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0
            
            # Calculate algorithm score (0-100)
            # 40% consistency, 30% frequency, 30% engagement
            frequency_score = min(100, (30 / max(avg_gap, 1)) * 100)
            consistency_score = consistency
            engagement_score = min(100, engagement_rate * 10)
            
            algorithm_score = int(
                (0.4 * consistency_score) +
                (0.3 * frequency_score) +
                (0.3 * engagement_score)
            )
            
            # Generate recommendations
            recommended_days = self._recommend_upload_days(upload_dates)
            view_prediction = int(avg_views * 1.1)  # Predict 10% growth
            
            # Generate AI growth suggestions
            channel_data = {
                'total_videos': len(videos),
                'avg_gap_days': round(avg_gap, 1),
                'consistency_score': round(consistency, 1),
                'engagement_rate': round(engagement_rate, 2),
                'algorithm_score': algorithm_score
            }
            
            try:
                growth_suggestions = gemini_client.generate_growth_suggestions(channel_data)
            except AIServiceUnavailable:
                growth_suggestions = self._fallback_suggestions(algorithm_score, avg_gap)
            
            return {
                'channel_id': channel_id,
                'algorithm_score': algorithm_score,
                'total_videos': len(videos),
                'shorts_count': len(shorts),
                'regular_count': len(regular),
                'consistency_metrics': {
                    'avg_gap_days': round(avg_gap, 1),
                    'consistency_score': round(consistency, 1),
                    'frequency_score': round(frequency_score, 1),
                    'engagement_score': round(engagement_score, 1)
                },
                'performance': {
                    'avg_views': int(avg_views),
                    'total_views': total_views,
                    'engagement_rate': round(engagement_rate, 2)
                },
                'upload_schedule': {
                    'recommended_days': recommended_days,
                    'current_avg_gap': round(avg_gap, 1)
                },
                'view_predictions': {
                    'next_video': view_prediction,
                    'based_on_avg': int(avg_views)
                },
                'growth_suggestions': growth_suggestions
            }
        except YouTubeAPIError as e:
            logger.error(f'YouTube API error in upload streak analysis: {str(e)}')
            return {'channel_id': channel_id, 'error': str(e), 'algorithm_score': 0}
    
    def _is_short_video(self, duration: str) -> bool:
        """Check if video is a Short (≤60 seconds)."""
        if not duration:
            return False
        
        # Parse ISO 8601 duration (e.g., PT1M30S, PT45S)
        import re
        match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return False
        
        minutes = int(match.group(1) or 0)
        seconds = int(match.group(2) or 0)
        total_seconds = (minutes * 60) + seconds
        
        return total_seconds <= 60
    
    def _recommend_upload_days(self, upload_dates: list) -> list:
        """Recommend best upload days based on historical data."""
        if not upload_dates:
            return ['Monday', 'Thursday']
        
        # Count uploads by day of week
        day_counts = {i: 0 for i in range(7)}
        for date in upload_dates:
            day_counts[date.weekday()] += 1
        
        # Get top 2 days
        sorted_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        return [day_names[day[0]] for day in sorted_days[:2]]
    
    def _fallback_suggestions(self, algorithm_score: int, avg_gap: float) -> list:
        """Fallback growth suggestions if AI unavailable."""
        suggestions = []
        
        if algorithm_score < 50:
            suggestions.append('Increase upload consistency to improve algorithm performance')
        
        if avg_gap > 7:
            suggestions.append('Upload more frequently - aim for at least once per week')
        
        if algorithm_score >= 70:
            suggestions.append('Great consistency! Keep maintaining your upload schedule')
        
        suggestions.append('Engage with comments to boost engagement metrics')
        suggestions.append('Optimize thumbnails and titles for better click-through rates')
        
        return suggestions
    
    def search_thumbnails(self, query: str = None, image_url: str = None) -> dict:
        """Search for thumbnails by text query or image similarity."""
        try:
            if query:
                return self._search_by_text(query)
            elif image_url:
                return self._search_by_image(image_url)
            else:
                return {'results': [], 'error': 'No search criteria provided'}
        except Exception as e:
            logger.error(f'Thumbnail search error: {str(e)}')
            return {'results': [], 'error': str(e)}
    
    def _search_by_text(self, query: str) -> dict:
        """Search videos by text query."""
        try:
            videos = youtube_client.search_videos(query, max_results=20)
            
            results = []
            for video in videos:
                # Calculate days since publish
                publish_date = datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - publish_date).days
                days_old = max(1, days_old)
                
                # Calculate views per day
                views_per_day = video['views'] / days_old
                
                # Calculate engagement rate
                total_engagement = video['likes'] + video['comments']
                engagement_rate = (total_engagement / video['views'] * 100) if video['views'] > 0 else 0
                
                results.append({
                    'video_id': video['id'],
                    'title': video['title'],
                    'thumbnail_url': video['thumbnail_url'],
                    'channel_title': video['channel_title'],
                    'views': video['views'],
                    'likes': video['likes'],
                    'comments': video['comments'],
                    'publish_date': video['publish_date'],
                    'views_per_day': round(views_per_day, 2),
                    'engagement_rate': round(engagement_rate, 2),
                    'days_old': days_old
                })
            
            return {
                'search_type': 'text',
                'query': query,
                'total_results': len(results),
                'results': results
            }
        except YouTubeAPIError as e:
            logger.error(f'YouTube API error in text search: {str(e)}')
            return {'results': [], 'error': str(e)}
    
    def _search_by_image(self, image_url: str) -> dict:
        """Search videos by image similarity using AI tags."""
        try:
            # Generate AI tags for the image
            tags = gemini_client.analyze_thumbnail(image_url)
            
            if not tags:
                return {'results': [], 'error': 'Could not generate tags for image'}
            
            # Use the first few tags as search query
            search_query = ' '.join(tags[:3])
            
            # Search videos using generated tags
            videos = youtube_client.search_videos(search_query, max_results=15)
            
            results = []
            for video in videos:
                publish_date = datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - publish_date).days
                days_old = max(1, days_old)
                
                views_per_day = video['views'] / days_old
                total_engagement = video['likes'] + video['comments']
                engagement_rate = (total_engagement / video['views'] * 100) if video['views'] > 0 else 0
                
                results.append({
                    'video_id': video['id'],
                    'title': video['title'],
                    'thumbnail_url': video['thumbnail_url'],
                    'channel_title': video['channel_title'],
                    'views': video['views'],
                    'likes': video['likes'],
                    'comments': video['comments'],
                    'publish_date': video['publish_date'],
                    'views_per_day': round(views_per_day, 2),
                    'engagement_rate': round(engagement_rate, 2),
                    'days_old': days_old
                })
            
            return {
                'search_type': 'image',
                'image_url': image_url,
                'generated_tags': tags,
                'search_query': search_query,
                'total_results': len(results),
                'results': results
            }
        except (YouTubeAPIError, AIServiceUnavailable) as e:
            logger.error(f'Error in image search: {str(e)}')
            return {'results': [], 'error': str(e)}
