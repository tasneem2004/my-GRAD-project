import pandas as pd
# here i import the pandas libary to read CSV (comma-separated values) files and name it pd for short

def read_quiz_csv(file_path):
    # methoud that Organizes our code, makes it reusable

    try:# try and except block to handle potential errors

        # read the CSV file into a DataFrame like a spreadsheet then stores it in a variable called df
                # FIX: Added encoding='utf-8-sig' to handle Windows files

        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print("Quiz Questions loaded successfully!")
        print("=" * 50)
        #with this the quiz questions will be displayed in the terminal
        
        # Display each question with its options
        for index, row in df.iterrows():
        # loop through each question in our Data one by one
            print(f"question {index + 1}: {row['question']}")
            #display the question to user
            print(f"A) {row['option_a']}")
            print(f"B) {row['option_b']}")
            print(f"C) {row['option_c']}")
            print(f"D) {row['option_d']}")
            print(f"✅ Correct answer: {row['correct_answer']}")
            print("-"*40)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    


    
#----------------------------------------------------------------

def main():
    #main function to test the read_quiz_csv function

    #path to the CSV file
    csv_file = "data/quiz_questions.csv" 
    print("QUIZ READER SCRIPT")
    print("=" * 30)

    #Read and display the quiz questions
    quiz_data = read_quiz_csv(csv_file)

    if quiz_data is not None:
        print(f"\n loaded {len(quiz_data)} questions successfully!")


#this make the script run when en execute it
if __name__ == "__main__":
    main()

       
