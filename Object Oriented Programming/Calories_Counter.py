# time for adding wait time to the prompts as they appear
import time
import os

# Seems like a good wait time
wait_time = 1.55

class Customer_care:
    '''The Customer_care class interacts with the user on a personal level. 
    It welcomes the user, provides instructions about the survey and 
    describes the features of the application. It does not ask the 
    survey questions, gather data from the user or provide recommendations. 
    It stores all the survey objects created by the application and allows for
    adding, editing or deleting survey objects.
    '''
    
    global wait_time

    def __init__(self):
        '''Method to create a Customer_care object to perform the duties assigned to it. 
        '''
        
        # list to store the surveys that are created.
        self.survey_list = []
           
    
    def welcome(self):
        '''Method to welcome the user to the application and provide information
        about what the application can do.
        '''
        print('-'*70)
        time.sleep(wait_time)
        print('Welcome to the calorie counter survey.')
        time.sleep(wait_time)
        print('This app will help you understand how to reach your weight goals.')
        time.sleep(wait_time)
        print('Or, if you are already perfect, just give you some interesting information.')
        time.sleep(wait_time)
        print('In any case, it will be fun.')
        time.sleep(wait_time)
        print('-'*70)
        
        
    def ask_response(self):
        '''Method to provide instructions to the user and ask what they would like to do.
        '''
        
        # Asking for response
        time.sleep(wait_time)
        print('You can add a survey (A), view an existing survey (V), delete an existing survey (D) or quit (Q)')
        time.sleep(wait_time)
        response = input('Please enter a response: ').upper()
        
        # Checking to make sure response is valid.
        if len(response) != 1 or response not in 'AVDQ':
            time.sleep(wait_time)
            print('Please enter \'A\', \'V\', \'D\' or \'Q\'')
            time.sleep(wait_time)
            
        return response
        
    
    def add_survey(self):
        '''Method to add a new survey.
        '''
        while True:
            try:
                label = input('Please enter a label for this new survey: ')

                # Checking if a label is already taken
                for survey in self.survey_list:
                    if survey.label == label:
                        time.sleep(wait_time)
                        print('Sorry, this label is already taken, please enter another label. ')
                        break
                else:
                    C.survey_list.append(Survey(label))
                    break

            # Input Error will end the current survey and go back to the main prompt
            except InputError:
                pass
    
        
    def view_survey(self):
        '''Method to view an existing survey.
        '''
        
        
        # Check if there are any surveys in the system
        if self.survey_list:
            
            # Show the list of surveys already in the system
            time.sleep(wait_time)
            
            print('Here is a list of surveys currently in the system.')
            time.sleep(wait_time)
            for survey in self.survey_list:
                print(str(self.survey_list.index(survey)) + ') ' + survey.label)

            time.sleep(wait_time)
            print('-'*70)
            
            
            # Ask for which survey needs to be viewed, with some error checking
            while True:
                
                try:            
                    self.survey_list[int(input('Enter the serial number of the survey you would like to view (0)-(' 
                                      + str(len(self.survey_list)-1) + '): '))].view()
                    print('-'*70)
                    break
                
                except ValueError:
                    time.sleep(wait_time)
                    print('Invalid Entry. Please enter an integer in the correct range.')
                    continue
                    
                except IndexError:
                    time.sleep(wait_time)
                    print('Invalid Entry.')
                    continue
        
        # No surveys in the system to view
        else:
            time.sleep(wait_time)
            print('Sorry, there are currently no surveys in the system.')
            time.sleep(wait_time)
            print('Try adding a new survey.')


    
    def delete_survey(self):
        '''Method to delete an existing survey.;
        '''
        
        
        # Check if there are any surveys in the system
        if self.survey_list:
            
            # Show the list of surveys already in the system
            time.sleep(wait_time)
            print('Here is a list of surveys currently in the system.')
            time.sleep(wait_time)
        
            for survey in self.survey_list:
                print(str(self.survey_list.index(survey)) + ') ' + survey.label)

            time.sleep(wait_time)
            
            
            # Ask for which survey needs to be deleted, with some error checking
            while True:
                
                try:
                    # Deleting a survey based on index            
                    del self.survey_list[int(input('Enter the serial number of the survey you would like to delete (0)-(' 
                                                   + str(len(self.survey_list)-1) + '): '))]
                    
                    time.sleep(wait_time)
                    print('Deleted!')
                    break

                except ValueError:
                    time.sleep(wait_time)
                    print('Invalid Entry. Please enter an integer')
                    continue
                    
                except IndexError:
                    time.sleep(wait_time)
                    print('Invalid Entry. Please enter an integer in the correct range.')
                    continue
        
        # No surveys in the system to delete
        else:
            time.sleep(wait_time)
            print('Sorry, there are currently no surveys in the system.')
            time.sleep(wait_time)
            print('Try adding a new survey.')
    

    
    
class Survey:
    '''The Survey class interacts with the user for gathering data. It sends the user to 
    the User_info class and the Exercise class for gathering data. It stores a User_info 
    object and a Exercise object in a dictionary. It also receives Recommendation objects
    from the Recommendation class and stores the Recommendations in the dictionary. It allows
    the user to view the information they have previously stored.
    '''
    
    global wait_time


    
    def __init__(self, label):
        '''Method to create a survey object.
        '''
        time.sleep(wait_time)

        # Input label to keep track of surveys
        
        self.label = label
        
        # Dict to store other objects created in the survey
        self.survey_dict = {}

        # Calling __init__ functions for each of the object that is part of the survey
        self.survey_dict['Goal'] = Goal()
        self.survey_dict['User_info'] = User_info()
        self.survey_dict['Exercise'] = Exercise()
        self.survey_dict['Recommendation'] = Recommendation(self.survey_dict['Goal'], \
                                                            self.survey_dict['User_info'], \
                                                            self.survey_dict['Exercise'])
               
    
    def view(self):
        '''Method to edit the survey object
        '''

        # Print each object stored in the survey_dict using each of their __repr__ functions
        time.sleep(wait_time)
        print('For ' + self.label + ' the following information was entered.')
        time.sleep(wait_time)
        print(self.survey_dict['User_info'])
        time.sleep(wait_time)
        print(self.survey_dict['Exercise'])
        time.sleep(wait_time)
        print('And recommendation was:')
        print(self.survey_dict['Recommendation'])
        
    
    
    
class Goal:
    '''The Goal class records the goal of the user. The goal can be to maintain weight, lose weight or gain weight'''
    
    def __init__(self):
        '''Method to create a Goal object'''
        
        # Input for goal with some error checking
        time.sleep(wait_time)
        print('Please enter your goal from this survey.')
        time.sleep(wait_time)
        while True:
            
            try:

                # Setting a goal as maintian, lose or gain
                time.sleep(wait_time)
                goal_input = int(input('Enter (0) for maintian weight, (1) for lose weight or (2) for gain weight: '))
                
                if goal_input not in [0, 1, 2]:
                    time.sleep(wait_time)
                    print('Invalid entry. Please enter 0, 1 or 2')
                                        
                else:
                    if goal_input == 0:
                        self.goal = 'maintain'
                    elif goal_input == 1:
                        self.goal = 'lose'
                    elif goal_input == 2:
                        self.goal = 'gain'
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Invalid entry. Please enter 0, 1 or 2.')
        

        
class User_info:
    '''The User_info class's main purpose is to store the user related data gathered from the 
    user. It also processes the user data to calculate additional parameters required to provide
    a recommendation.
    '''
    
    global wait_time
    
    def __init__(self):
        '''Method to create a User_info object.'''
        
        # Creating User_info object, and populating using the populate function        
        time.sleep(wait_time)
        print('First, we need some some information about you.')
        time.sleep(wait_time)
        print('Please follow the prompts to enter your infomation.')
        self.populate()
        
        
    
    
    def populate(self):
        '''Method to populate the User_info object by gathering data from the user.'''
        time.sleep(wait_time)
        print('-'*70)
        
        # Input age with some error checking
        while True:
            
            try:

                # Input age from the user. If age is ourside range, survey ends and goes back to the main prompt
                time.sleep(wait_time)
                age_input = int(input('Please enter your age in years (18-65): '))
                
                if age_input < 18 or age_input > 65:
                    time.sleep(wait_time)
                    print('Sorry, this survey is only for adults between 18-65 years old.')
                    raise InputError
                    
                else:
                    self.age = age_input
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Please enter an integer as your age.')
         
        
        # Input sex with some error checking        
        while True:
            
            try:

                # Input sex from the user. Keep asking until a valid option is entered.
                time.sleep(wait_time)
                sex_input = int(input('Please enter your sex, (0) for male, (1) for female: '))
                
                if sex_input not in [0, 1]:
                    time.sleep(wait_time)
                    print('Invalid entry. Please enter 0 or 1')
                                        
                else:
                    if sex_input == 0:
                        self.sex = 'male'
                    elif sex_input == 1:
                        self.sex = 'female'
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Invalid entry. Please enter 0 or 1.')
                
                
        # Input height (feet) with some error checking        
        while True:
            
            try:

                # Input height in feet from the user. If height is outside the range, survey ands and goes back to the main prompt
                time.sleep(wait_time)
                print('Please enter your height in feet and inches in the following 2 prompts')
                time.sleep(wait_time)
                feet_input = int(input('Feet (4-7): '))
                
                if feet_input < 4 or feet_input > 7:
                    time.sleep(wait_time)
                    print('Sorry, this only works for people with height between 4 feet to 7 feet.')
                    raise InputError
                                        
                else:
                    self.height = feet_input*12
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Invalid entry. Please enter an integer between 4 and 7.')
                
         
        # Input height (inches) with some error checking
        while True:
            
            # Input height in inches from the user. Keep asking for input unitl a valid answer is entered
            try:
                time.sleep(wait_time)
                inches_input = int(input('Inches: '))
                
                if inches_input < 0 or inches_input > 11:
                    time.sleep(wait_time)
                    print('Please enter an integer from 0 to 11.')
                                                            
                else:
                    self.height += inches_input
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Invalid entry. Please enter an integer from 0 to 11.')
                
                
        # Input weight with some error checking
        while True:
            
            # Input weight from the user. If weight is outside the range, survey ands and goes back to the main prompt
            try:
                time.sleep(wait_time)
                weight_input = int(input('Please enter your weight in lbs (50-450): '))
                
                if weight_input < 50 or weight_input > 450:
                    time.sleep(wait_time)
                    print('Sorry, this only works for people with weight between 50 lbs to 450 lbs.')
                    raise InputError
                                                            
                else:
                    self.weight = weight_input
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Invalid entry. Please enter an integer from 50 to 450.')
         
        # Calculate Body Mass Index and Basal Metabolic Rate of the user       
        self.calculate_BMI()  
        self.calculate_BMR()
                    
    
    
    def calculate_BMI(self):
        '''Method to calculate the Body Mass Index of a person'''
        self.BMI = round(703*self.weight/((self.height)**2), 1)
        
        
    
    
    def calculate_BMR(self):
        '''Method to calculate the Basal Metabolic Rate of a Person'''
        if self.sex == 'male':
            self.BMR = 13.397*self.weight/2.204 + 4.799*self.height*2.54 - 5.677*self.age + 88.362
        elif self.sex == 'female':
            self.BMR = 9.247*self.weight/2.204 + 3.098*self.height*2.54 - 4.330*self.age + 447.593
    

    def __repr__(self):
        '''Method to print stored User_info object'''
        return ('Age = ' + str(self.age) + '\nSex = ' + self.sex + '\nHeight = ' \
                + str(self.height//12) + ' feet ' + str(self.height%12) + ' inches'\
               + '\nWeight = ' + str(self.weight))
        
            

        
class Exercise:
    '''The Exercise class's main purpose is to store the exercise related data gathered from the
    user. It also processes the exercise data to calculate additional parameters required to provide
    a recommendation.
    ''' 
    
    global wait_time
    
    def __init__(self):
        '''Method to create an Exercise object.'''

        # Create Exercise object and call populate to populate all the fields
        time.sleep(wait_time)
        print('Let\'s get some information about your physical activity.')
        time.sleep(wait_time)
        print('Please follow the prompts to enter your infomation.')
        self.populate()
        
        
    def populate(self):
        '''Method to populate the Exercise object by gathering data from the user.'''
        # Input exercise frequency with some error checking
        print('-'*70)
        while True:
            
            # Input exercise frequency. Keep asking for input until a valid input is entered
            try:
                time.sleep(wait_time)
                freq_input = int(input('Please enter you exercise frequency per week (0-7): '))
                
                if freq_input < 0 or freq_input > 7:
                    time.sleep(wait_time)
                    print('Please enter an integer from 0 to 7.')
                    
                    
                else:
                    self.freq = freq_input
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Please enter an integer as your exercise frequency.')
                
        
        # Input exercise intensity with some error checking
        while True:
            
            # If frequency was entered as 0, no intensity is asked for.
            if self.freq == 0:
                self.intensity = 'Light'
                break
            
            # Asking for input on the exercise intensity. Keep asking for input until a valid input is entered
            try:
                time.sleep(wait_time)
                intensity_input = int(input('Please enter you exercise intensity (0) for light, (1) for intense: '))
                
                if intensity_input not in [0, 1]:
                    time.sleep(wait_time)
                    print('Please enter 0 or 1.')
                    
                    
                else:
                    if intensity_input == 0:
                        self.intensity = 'Light'
                    elif intensity_input == 1:
                        self.intensity = 'Intense'
                    break
            
            except ValueError:
                time.sleep(wait_time)
                print('Please enter 0 or 1 as your exercise intensity.')
        
        # Call function to calculate exercise level        
        self.calculate_exercise_level()
   

    def calculate_exercise_level(self):
        '''Method to categorize exercise into differnet levels based on intensity and frequency.'''
        
        # Levels of light exercise based on frequency
        if self.intensity == 'Light':
            if self.freq == 0:
                self.exercise_level = 0
            elif self.freq > 0 and self.freq <= 3:
                self.exercise_level = 1
            elif self.freq > 3 and self.freq <= 5:
                self.exercise_level = 2
            elif self.intfreqensity > 5 and self.freq <= 7:
                self.exercise_level = 3
        
        # Levels of intense exercise based on frequency
        elif self.intensity == 'Intense':
            if self.freq == 0:
                self.exercise_level = 0
            elif self.freq > 0 and self.freq <= 2:
                self.exercise_level = 2
            elif self.freq > 2 and self.freq <= 4:
                self.exercise_level = 3
            elif self.freq > 4 and self.freq <= 7:
                self.exercise_level = 4
                
    def __repr__(self):
        '''Method to print stored Exercise object'''
        return (self.intensity + ' exercise, ' + str(self.freq) + ' time per week.')
                

class Recommendation:
    '''The Recommendation class accesses and proccesses the data stored in the User_info and Exercise 
    objects to create a Recommendation object that contains information about recommendations to be 
    provided to the user.
    '''
    
    global wait_time
    
    def __init__(self, Goal, User_info, Exercise):
        '''Method to create a Recommendation object.'''

        # Create a Recommendation object
        time.sleep(wait_time)
        print('Calculating your recommendation...')
        self.calculate_BMI_reco(Goal, User_info, Exercise)
        self.calculate_cals_reco(Goal, User_info, Exercise)
        print(self)
              
    
    def calculate_BMI_reco(self, Goal, User_info, Exercise):
        '''Method to calculate a recommendation based on the BMI of the user'''

        # Underweight BMI
        if User_info.BMI < 18.5:
            self.BMI_reco = 'Your Body Mass Index is ' + str(User_info.BMI) \
            + '. It indicates that you are underweight.'

            # Change goal to gain weight if it wasn't already
            if Goal.goal != 'gain':

                # Add a suggestion statement to the recommendation
                self.BMI_reco += ' It is suggested that you try to gain weight.'
                Goal.goal = 'gain'
        
        # Normal BMI    
        elif User_info.BMI >= 18.5 and User_info.BMI < 25:
            self.BMI_reco = 'Your Body Mass Index is ' + str(User_info.BMI) \
            + '. It indicates that you are in the normal weight range.'
        

        # Overweight BMI    
        elif User_info.BMI >= 25 and User_info.BMI < 30:
            self.BMI_reco = 'Your Body Mass Index is ' + str(User_info.BMI) \
            + '. It indicates that you are overweight.'

            # Change goal to lose weight if it wasn't already
            if Goal.goal != 'lose':

                # Add a suggestion statement to the recommendation
                self.BMI_reco += ' It is suggested that you try to lose weight.'
                Goal.goal = 'lose'
        

        # Obese BMI    
        elif User_info.BMI > 30:            
            self.BMI_reco = 'Your Body Mass Index is ' + str(User_info.BMI) \
            + '. It indicates that you are obese.'

            # Change goal to lose weight if it wasn't already
            if Goal.goal != 'lose':

                # Add a suggestion statement to the recommendation
                self.BMI_reco += ' It is suggested that you try to lose weight.'
                Goal.goal = 'lose'
                
        
    
    
    def calculate_cals_reco(self, Goal, User_info, Exercise):
        '''Method to calculate the calorie intake required to maintain, reduce or increase the
        current weight of the user.
        '''
        
        # Calories to maintian formula based on exercise level
        if Exercise.exercise_level == 0:
            cals_for_maintain = 1.2*User_info.BMR

        elif Exercise.exercise_level == 1:
            cals_for_maintain = 1.37*User_info.BMR

        elif Exercise.exercise_level == 2:
            cals_for_maintain = 1.46*User_info.BMR

        elif Exercise.exercise_level == 3:
            cals_for_maintain = 1.54*User_info.BMR

        elif Exercise.exercise_level == 4:
            cals_for_maintain = 1.72*User_info.BMR
        
        # Rounding to nearest 50    
        cals_for_maintain = int(cals_for_maintain)//50*50
                
            
        # Recommended calories based on goal    
        if Goal.goal == 'maintain':
            self.cal_reco = 'You need to consume ' \
            + str(cals_for_maintain) + ' calories per day to maintain your current weight.'
        elif Goal.goal == 'lose':
            self.cal_reco = 'You need to consume ' \
            + str(cals_for_maintain - 500)  + ' calories per day to lose 1 lb per week.'
        elif Goal.goal == 'gain':
            self.cal_reco = 'You need to consume ' \
            + str(cals_for_maintain + 500)  + ' calories per day to gain 1 lb per week.'
            
            
    def __repr__(self):
        '''Method to print the recommendation generated by the application.'''
        return (self.BMI_reco) + '\n' + (self.cal_reco)
        
  
# InputError indicates when to abondon the survey and go bac kto the main prompt
class InputError(Exception):
    pass


    

# MAIN PROGRAM:  CALORIE COUNTER APP

# Create a Customer_care object
C = Customer_care()

# Welcoming user
C.welcome()

response = ''

# Asking what the user would like to do
while response != 'Q':
    response = C.ask_response().upper()
    print('-'*70)
    
    if response == 'A':
        C.add_survey()
    elif response == 'V':
        C.view_survey()
    elif response == 'D':
        C.delete_survey()

# Thank user when they quit        
time.sleep(wait_time)
print('Thanks for using the Calorie Calculator!')
time.sleep(wait_time)
    
    

    
    


