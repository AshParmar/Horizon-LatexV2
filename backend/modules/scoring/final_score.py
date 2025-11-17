"""
Final Score Calculator Module

TODO: Combine LLM and keyword scores into final score
Contributors: Implement weighted scoring and ranking logic
"""

from typing import Dict, Any


class FinalScoreCalculator:
    """
    Final Score Calculator
    
    TODO: Implement weighted score combination
    """
    
    def __init__(
        self,
        llm_weight: float = 0.6,
        keyword_weight: float = 0.4
    ):
        """
        Initialize Final Score Calculator
        
        Args:
            llm_weight: Weight for LLM score (0-1)
            keyword_weight: Weight for keyword score (0-1)
        """
        self.llm_weight = llm_weight
        self.keyword_weight = keyword_weight
        
        if abs(llm_weight + keyword_weight - 1.0) > 0.01:
            raise ValueError("Weights must sum to 1.0")
    
    
    def calculate_final_score(
        self,
        llm_score: float,
        keyword_score: float,
        llm_details: Dict[str, Any],
        keyword_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate final weighted score
        
        TODO: Implement score calculation
        - Weighted average of scores
        - Normalize scores if needed
        - Generate score breakdown
        - Add confidence level
        
        Args:
            llm_score: Score from LLM (0-1)
            keyword_score: Score from keyword matching (0-1)
            llm_details: Detailed LLM scoring
            keyword_details: Detailed keyword scoring
            
        Returns:
            Final score with breakdown
        """
        final_score = (
            self.llm_weight * llm_score +
            self.keyword_weight * keyword_score
        )
        
        return {
            "final_score": final_score,
            "llm_score": llm_score,
            "keyword_score": keyword_score,
            "weights": {
                "llm": self.llm_weight,
                "keyword": self.keyword_weight
            },
            "breakdown": {
                "llm_details": llm_details,
                "keyword_details": keyword_details
            },
            "recommendation": self.generate_recommendation(final_score)
        }
    
    
    def generate_recommendation(self, score: float) -> str:
        """
        Generate hiring recommendation based on score
        
        TODO: Customize thresholds
        - Strong match: > 0.75
        - Good match: 0.6 - 0.75
        - Potential: 0.5 - 0.6
        - Weak: < 0.5
        
        Args:
            score: Final score (0-1)
            
        Returns:
            Recommendation string
        """
        if score >= 0.75:
            return "strong_match"
        elif score >= 0.6:
            return "good_match"
        elif score >= 0.5:
            return "potential"
        else:
            return "weak_match"
    
    
    def rank_candidates(
        self,
        candidate_scores: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Rank candidates by final score
        
        TODO: Implement ranking logic
        - Sort by final score
        - Add rank position
        - Group by recommendation
        
        Args:
            candidate_scores: List of candidate score dicts
            
        Returns:
            Sorted list with rankings
        """
        # Sort by final_score descending
        sorted_candidates = sorted(
            candidate_scores,
            key=lambda x: x.get("final_score", 0),
            reverse=True
        )
        
        # Add rank
        for i, candidate in enumerate(sorted_candidates):
            candidate["rank"] = i + 1
        
        return sorted_candidates
    
    
    def calculate_percentile(
        self,
        score: float,
        all_scores: list[float]
    ) -> float:
        """
        Calculate percentile of a score
        
        TODO: Implement percentile calculation
        - Shows how candidate ranks relative to others
        
        Args:
            score: Candidate's score
            all_scores: All scores in pool
            
        Returns:
            Percentile (0-100)
        """
        if not all_scores:
            return 0.0
        
        count_below = sum(1 for s in all_scores if s < score)
        percentile = (count_below / len(all_scores)) * 100
        
        return percentile
