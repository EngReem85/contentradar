import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class Dashboard:
    """Analytics dashboard"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_stats(self) -> Dict[str, Any]:
        """Get basic statistics"""
        stats = {
            'total_items': len(self.df),
            'content_types': self.df['content_type'].value_counts().to_dict(),
            'sources': self.df['source'].value_counts().to_dict(),
        }
        
        if 'popularity' in self.df.columns:
            stats['avg_popularity'] = float(self.df['popularity'].mean())
            stats['max_popularity'] = float(self.df['popularity'].max())
        
        if 'metadata' in self.df.columns:
            ratings = []
            for meta in self.df['metadata']:
                if isinstance(meta, dict) and 'vote_average' in meta:
                    ratings.append(meta['vote_average'])
            if ratings:
                stats['avg_rating'] = sum(ratings) / len(ratings)
        
        return stats
    
    def create_content_distribution_chart(self):
        """Create content distribution chart"""
        if 'content_type' not in self.df.columns:
            return None
        
        counts = self.df['content_type'].value_counts()
        fig = px.pie(
            values=counts.values,
            names=counts.index,
            title="Content Distribution by Type",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        return fig
    
    def create_popularity_chart(self, top_n: int = 20):
        """Create popularity chart"""
        if 'popularity' not in self.df.columns:
            return None
        
        top_items = self.df.nlargest(top_n, 'popularity')
        fig = px.bar(
            top_items,
            x='title',
            y='popularity',
            title=f"Top {top_n} Most Popular Content",
            color='content_type'
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig
    
    def create_source_distribution(self):
        """Create source distribution chart"""
        if 'source' not in self.df.columns:
            return None
        
        counts = self.df['source'].value_counts()
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            title="Content by Source",
            labels={'x': 'Source', 'y': 'Count'}
        )
        return fig