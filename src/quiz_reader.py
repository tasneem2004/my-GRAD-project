import pandas as pd
import random

class QuizReader:
    def __init__(self, csv_file="quiz_questions.csv"):
        self.csv_file = csv_file
        self.questions_df = self.load_questions()
    
    def load_questions(self):
        """Load questions from CSV file"""
        try:
            df = pd.read_csv(self.csv_file)
            # Ensure expected columns exist
            required_columns = ['question', 'options', 'correct_answer', 'difficulty', 'topic']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            return df
        except Exception as e:
            print(f"Error loading questions: {e}")
            return pd.DataFrame()
    
    def get_questions_by_difficulty(self, difficulty_level, topic=None, limit=5):
        """Get questions filtered by difficulty and optionally by topic"""
        filtered_df = self.questions_df[self.questions_df['difficulty'] == difficulty_level]
        
        if topic:
            filtered_df = filtered_df[filtered_df['topic'] == topic]
        
        if len(filtered_df) > 0:
            # Return random selection of questions
            return filtered_df.sample(min(limit, len(filtered_df))).to_dict('records')
        else:
            # Fallback to any questions at this difficulty level
            fallback_df = self.questions_df[self.questions_df['difficulty'] == difficulty_level]
            return fallback_df.sample(min(limit, len(fallback_df))).to_dict('records')
    
    def get_all_topics(self):
        """Get list of all available topics"""
        return self.questions_df['topic'].unique().tolist()
       
