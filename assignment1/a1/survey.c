#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_WORDS 1100
#define MAX_WORD_LEN 1100
#define MAX_LINE_LEN 50000
#define MAX 100

/* tokenizes each line by splitting words 
    and stores them in a string array */
int tokenize_line(char *line, char words[][MAX_WORD_LEN], int num_lines, const char* delimiter) {

    //int num_lines = 0;
    char *token;
    
    /* get the first token from line */
    token = strtok(line, delimiter);
    
    /* for every token in line, store it */
    while (token) {

        strncpy(words[num_lines], token, MAX_WORD_LEN);
        num_lines++;
        
        /* get the next token from line or reach end of line */
        token = strtok(NULL, delimiter);
    } 
    return num_lines;           
}

// extracts just the answers from the responses array (removes faculty and other info)
void extract_answers(int total_responses,  char responses[MAX_WORDS][MAX_WORD_LEN], char answers[100][100][100]) {
    for (int i = 0; i < total_responses; i++) {
        int num_words = 0;

        // tokenize the response
        char *token = strtok(responses[i], ",");
        while (token) {
            if (num_words >= 3) { // skip the first three tokens
                strncpy(answers[i][num_words - 3], token, MAX_WORD_LEN); // store answers
            }
            num_words++;
            token = strtok(NULL, ",");
        }
    }
}

// calculates the relative percentage frequency
void relative_percentage_frequency(int num_likert, int num_questions, double percentage_frequency[num_questions][num_likert], int num_responses, char question_type[][MAX_WORD_LEN], char answers[100][100][100]){
    double times_picked[num_questions][num_likert];
    memset(times_picked, 0, sizeof(times_picked));

    // tallies up how many times a certain option is picked per question
    for(int i = 0; i < num_questions; i ++){
        for(int j = 0; j < num_responses; j ++){
                
                if (strncmp("fully disagree", answers[j][i], 13) == 0) {
                    times_picked[i][0] += 1;
                } else if (strncmp("disagree", answers[j][i], 8) == 0) {
                    times_picked[i][1] += 1;
                } else if (strncmp("partially disagree", answers[j][i], 18) == 0) {
                    times_picked[i][2] += 1;
                } else if (strncmp("partially agree", answers[j][i], 15) == 0) {
                    times_picked[i][3] += 1;
                } else if (strncmp("agree", answers[j][i], 5) == 0) {
                    times_picked[i][4] += 1;
                } else if (strncmp("fully agree", answers[j][i], 10) == 0) {
                    times_picked[i][5] += 1;
                } 
        }
    }

    // calcualtes the precentage frequency
     for(int i = 0; i < num_questions; i ++){
        for(int j = 0; j < num_likert; j ++){
            percentage_frequency[i][j] = (times_picked[i][j]/num_responses) * 100;
        }
     }
     
} // relative_percentage_frequency

// converts the answers to linkert form depending on wheter it is direct or reverse
void convert_answers(int num_questions, int num_responses, int converted_answers[num_responses][num_questions], 
                     char question_type[][MAX_WORD_LEN], char answers[100][100][100]) {
    
    for (int i = 0; i < num_responses; i++) {
        for (int j = 0; j < num_questions; j++) {
            if (strncmp("Direct", question_type[j], 6) == 0 || strncmp("direct", question_type[j], 6) == 0) {
                if (strcmp("fully disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 1;
                } else if (strcmp("disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 2;
                } else if (strcmp("partially disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 3;
                } else if (strcmp("partially agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 4;
                } else if (strcmp("agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 5;
                } else if (strcmp("fully agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 6;
                }
            } else if (strncmp("Reverse", question_type[j], 7) == 0 || strncmp("reverse", question_type[j], 7) == 0) {
                if (strcmp("fully disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 6;
                } else if (strcmp("disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 5;
                } else if (strcmp("partially disagree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 4;
                } else if (strcmp("partially agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 3;
                } else if (strcmp("agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 2;
                } else if (strcmp("fully agree", answers[i][j]) == 0) {
                    converted_answers[i][j] = 1;
                }
            }
        } // for j
    } // for i

} // convert_answers

// calculates the scores per respondants per question tyep
void generate_scores(int num_questions, int num_responses, double scores[num_responses][5],
                     int converted_answers[num_responses][num_questions], 
                     char questions[MAX_WORDS][MAX_WORD_LEN]) {
    
    // Initialize scores to 0
    memset(scores, 0, sizeof(double) * num_responses * 5);

    // Sum up the responses per question
    for (int i = 0; i < num_responses; i++) {
        for (int j = 0; j < num_questions; j++) {
            if (i >= 0 && i <= 7) {
                scores[i][0] += converted_answers[i][j]; 
            } else if (i >= 9 && i <= 17) {
                scores[i][1] += converted_answers[i][j];
            } else if (i >= 18 && i <= 27) {
                scores[i][2] += converted_answers[i][j];
            } else if (i >= 28 && i <= 33) {
                scores[i][3] += converted_answers[i][j];
            } else if (i >= 34 && i <= 37) {
                scores[i][4] += converted_answers[i][j];
            }
        }
    }

    // Divide the accumulated scores for each group
    for (int j = 0; j < 5; j++) { // Iterate over the number of groups (5)
        for (int i = 0; i < num_responses; i++) {
            switch (j) {
                case 0:
                    scores[i][j] /= 8;  // C has 8 questions
                    break;
                case 1:
                    scores[i][j] /= 10; // I has 10 questions
                    break;
                case 2:
                    scores[i][j] /= 10; // G has 10 questions
                    break;
                case 3:
                    scores[i][j] /= 6;  // U  has 6 questions
                    break;
                case 4:
                    scores[i][j] /= 4;  // P has 4 questions
                    break;
            }
            
        }
        
    }
    
} // generate_scores


// averages the scores
void generate_average_score(int num_questions, int num_responses, double scores[num_responses][5], double average_scores[5]) {
    double sums[5] = {0.0};    

    // avoiding division by 0
    if (num_responses <= 0) {
        for (int i = 0; i < 5; i++) {
            average_scores[i] = 0.0; 
        }
        return;
    }

    // sum the scores for each category
    for (int i = 0; i < num_responses; i++) {
        for (int j = 0; j < 5; j++) {
            sums[j] += scores[i][j]; 
        }
    }

    // calculate the average for each category
    for (int i = 0; i < 5; i++) {
        average_scores[i] = sums[i] / num_responses;
    }
}

// prints the output to the terminal and formats the output
void generate_output(int num_responses, int num_questions, char questions[][MAX_WORD_LEN], int num_likert, 
                    char likert[MAX_WORDS][MAX_WORD_LEN], double percentage_frequency[num_questions][num_likert], 
                    char file_type[MAX_WORDS][MAX_WORD_LEN], double scores[num_responses][5], double average_scores[5]){
    printf("Examining Science and Engineering Students' Attitudes Towards Computer Science \nSURVEY RESPONSE STATISTICS\n");
    printf("\nNUMBER OF RESPONDENTS: %d\n", num_responses);
    printf("\nFOR EACH QUESTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n");
    
    if (strncmp("1", file_type[0], 1) == 0){
        for(int i = 0; i < num_questions; i ++){
            printf("\n%s\n", questions[i]);
            for(int j = 0; j < num_likert; j ++){
                printf("%.2f: %s\n", 0.0, likert[j]);
            }
        }
    }
    
    if (strncmp("1", file_type[1], 1) == 0){
        for(int i = 0; i < num_questions; i ++){
            printf("\n%s\n", questions[i]);
            printf("hellow");
            for(int j = 0; j < num_likert; j ++){
                printf("%.2f: %s\n", percentage_frequency[i][j], likert[j]);
            }
        }
    }
    if (strncmp("1", file_type[2], 1) == 0){
        printf("\nSCORES FOR ALL THE RESPONDENTS\n\n");
        
        for (int i = 0; i < num_responses; i++) {
            for (int j = 0; j < 5; j++) {
                switch (j) {
                    case 0:
                        printf("C:%.2f,", scores[i][j]); 
                        break;
                    case 1:
                        printf("I:%.2f,", scores[i][j]);
                        break;
                    case 2:
                        printf("G:%.2f,", scores[i][j]);
                        break;
                    case 3:
                        printf("U:%.2f,", scores[i][j]);
                        break;
                    case 4:
                        printf("P:%.2f", scores[i][j]);
                        break;
                } 

            }
            printf("\n");
        }
    }
    if (strncmp("1", file_type[3], 1) == 0){
        printf("\nAVERAGE SCORES PER RESPONDENT\n\n");
        for (int i = 0; i < 5; i ++) {
            switch (i) {
                case 0:
                    printf("C:%.2f,", average_scores[i]);
                    break;
                case 1:
                    printf("I:%.2f,", average_scores[i]);
                    break;
                case 2:
                    printf("G:%.2f,", average_scores[i]);
                    break;
                case 3:
                    printf("U:%.2f,", average_scores[i]);
                    break;
                case 4:
                    printf("P:%.2f", average_scores[i]);
                    break;
                } 
        } // for
        printf("\n");
    }
    
} // generate_output

int main() {
    int num_questions = 0;
    int num_likert = 0;
    int num_responses = 0;

    char questions[MAX_WORDS][MAX_WORD_LEN];
    char likert[MAX_WORDS][MAX_WORD_LEN];
    char question_type[MAX_WORDS][MAX_WORD_LEN];
    char file_type[MAX_WORDS][MAX_WORD_LEN];
    char responses[MAX_WORDS][MAX_WORD_LEN];
    char answers[100][100][100];

    char line[MAX_LINE_LEN];
    int count = 0;

    double percentage_frequency[num_questions][num_likert];
    double scores[num_responses][5];
    double average_scores[5] = {0};

    memset(percentage_frequency, 0, sizeof(percentage_frequency));  // Set all elements to 0

    // tokenzing each section of the input file
    while (fgets(line, sizeof(char) * MAX_LINE_LEN, stdin) ) {
        if (line[0] == '#') {
            continue;
        }
        switch (count){
            case 0:
                tokenize_line(line, file_type, 0, ",\n");
                break;
            case 1:
                num_questions = tokenize_line(line, questions, 0, ";\n");
                break;
            case 2: 
                tokenize_line(line, question_type, 0, ";\n");
                break;
            case 3: 
                num_likert = tokenize_line(line, likert, 0, ",\n");
                break;
            default:
                  num_responses = tokenize_line(line, responses, num_responses, "\n");
                break;
        }
        count ++;
    }   // while

    extract_answers(num_responses, responses, answers);
    int converted_answers [num_responses][num_questions];

    convert_answers(num_questions, num_questions, converted_answers, question_type, answers);
    relative_percentage_frequency(num_likert, num_questions, percentage_frequency, num_responses, question_type, answers);

    generate_scores(num_questions, num_responses, scores, converted_answers, questions);
    generate_average_score(num_questions, num_responses, scores, average_scores);
    
    generate_output(num_responses, num_questions, questions, num_likert, likert, percentage_frequency, file_type, scores, average_scores);
   return 0;
}
