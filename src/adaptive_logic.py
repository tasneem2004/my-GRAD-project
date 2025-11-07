#Track student performance (correct/incorrect answers, time spent)
#Adjust question difficulty based on performance
#Identify knowledge gaps and focus on weak areas
#Store progress for each student




import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

class AdaptiveTutor:
    def __init__(self, student_id):
        self.student_id = student_id
        self.student_file = f"data/student_{student_id}.json"
        self.performance_history = self.load_student_data()
        
        # Adaptive parameters
        self.difficulty_level = 1  # 1-5 scale
        self.consecutive_correct = 0
        self.consecutive_wrong = 0
        self.mastery_threshold = 3  # Correct answers needed to level up
        self.weak_areas = {}
        
    def load_student_data(self):
        """Load student data from JSON file, create if doesn't exist"""
        try:
            if os.path.exists(self.student_file):
                with open(self.student_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize new student record
                base_data = {
                    'student_id': self.student_id,
                    'created_at': datetime.now().isoformat(),
                    'total_questions_answered': 0,
                    'correct_answers': 0,
                    'average_score': 0.0,
                    'difficulty_progression': [1],
                    'topic_performance': {},
                    'session_history': []
                }
                self.save_student_data(base_data)
                return base_data
        except Exception as e:
            print(f"Error loading student data: {e}")
            return {}
    
    def save_student_data(self, data=None):
        """Save student data to JSON file"""
        if data is None:
            data = self.performance_history
            
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        try:
            with open(self.student_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving student data: {e}")
    
    def update_performance(self, question_data, was_correct, time_spent, topic):
        """Update student performance after answering a question"""
        
        # Update basic metrics
        self.performance_history['total_questions_answered'] += 1
        if was_correct:
            self.performance_history['correct_answers'] += 1
            self.consecutive_correct += 1
            self.consecutive_wrong = 0
        else:
            self.consecutive_correct = 0
            self.consecutive_wrong += 1
        
        # Calculate new average score
        total = self.performance_history['total_questions_answered']
        correct = self.performance_history['correct_answers']
        self.performance_history['average_score'] = correct / total if total > 0 else 0
        
        # Update topic performance
        if topic not in self.performance_history['topic_performance']:
            self.performance_history['topic_performance'][topic] = {
                'attempted': 0,
                'correct': 0,
                'average_time': 0
            }
        
        topic_data = self.performance_history['topic_performance'][topic]
        topic_data['attempted'] += 1
        if was_correct:
            topic_data['correct'] += 1
        
        # Update adaptive difficulty
        self._adjust_difficulty(was_correct, topic)
        
        # Add to session history
        session_entry = {
            'timestamp': datetime.now().isoformat(),
            'question_id': question_data.get('id', 'unknown'),
            'topic': topic,
            'was_correct': was_correct,
            'time_spent': time_spent,
            'difficulty_level': self.difficulty_level
        }
        self.performance_history['session_history'].append(session_entry)
        
        # Save updated data
        self.save_student_data()
        
        return self.difficulty_level
    
    def _adjust_difficulty(self, was_correct, topic):
        """Adjust question difficulty based on performance"""
        
        if was_correct:
            if self.consecutive_correct >= self.mastery_threshold:
                # Student is doing well, increase difficulty
                if self.difficulty_level < 5:
                    self.difficulty_level += 1
                    self.consecutive_correct = 0  # Reset counter
                    print(f"Difficulty increased to level {self.difficulty_level}")
        else:
            if self.consecutive_wrong >= 2:
                # Student is struggling, decrease difficulty
                if self.difficulty_level > 1:
                    self.difficulty_level -= 1
                    self.consecutive_wrong = 0  # Reset counter
                    print(f"Difficulty decreased to level {self.difficulty_level}")
        
        # Track weak areas (topics with < 60% accuracy)
        topic_data = self.performance_history['topic_performance'].get(topic, {})
        if topic_data.get('attempted', 0) >= 3:
            accuracy = topic_data.get('correct', 0) / topic_data.get('attempted', 1)
            if accuracy < 0.6:
                self.weak_areas[topic] = accuracy
        
        # Record difficulty progression
        self.performance_history['difficulty_progression'].append(self.difficulty_level)
    
    def get_recommendations(self):
        """Get personalized learning recommendations"""
        recommendations = []
        
        # Identify weakest topics
        weak_topics = sorted(self.weak_areas.items(), key=lambda x: x[1])[:3]
        for topic, accuracy in weak_topics:
            recommendations.append(f"Focus on {topic} (accuracy: {accuracy:.1%})")
        
        # General recommendations based on performance
        avg_score = self.performance_history['average_score']
        if avg_score < 0.5:
            recommendations.append("Consider reviewing fundamental concepts")
        elif avg_score > 0.8:
            recommendations.append("You're ready for more challenging material!")
        
        return recommendations
    
    def get_next_question_difficulty(self):
        """Determine appropriate difficulty for next question"""
        return self.difficulty_level

# Utility functions for CSV operations
def update_student_csv(student_id, performance_data):
    """Update main student records CSV file"""
    csv_file = "data/students_performance.csv"
    
    # Create CSV with headers if it doesn't exist
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=[
            'student_id', 'timestamp', 'total_questions', 'correct_answers', 
            'average_score', 'current_difficulty', 'weak_topics'
        ])
        df.to_csv(csv_file, index=False)
    
    # Read existing data
    df = pd.read_csv(csv_file)
    
    # Update or add student record
    mask = df['student_id'] == student_id
    weak_topics = json.dumps(list(performance_data.get('weak_areas', {}).keys()))
    
    new_row = {
        'student_id': student_id,
        'timestamp': datetime.now().isoformat(),
        'total_questions': performance_data['total_questions_answered'],
        'correct_answers': performance_data['correct_answers'],
        'average_score': performance_data['average_score'],
        'current_difficulty': performance_data['difficulty_progression'][-1],
        'weak_topics': weak_topics
    }
    
    if mask.any():
        df.loc[mask, list(new_row.keys())] = list(new_row.values())
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_csv(csv_file, index=False)

def export_student_report(student_id):
    """Generate a comprehensive report for a student"""
    json_file = f"data/student_{student_id}.json"
    
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        report = {
            'student_id': student_id,
            'report_generated': datetime.now().isoformat(),
            'overall_performance': {
                'total_questions': data['total_questions_answered'],
                'correct_answers': data['correct_answers'],
                'accuracy_rate': f"{data['average_score']:.1%}",
                'current_difficulty_level': data['difficulty_progression'][-1]
            },
            'topic_breakdown': data['topic_performance'],
            'learning_recommendations': AdaptiveTutor(student_id).get_recommendations()
        }
        
        # Save report
        report_file = f"data/student_{student_id}_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    return None