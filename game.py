import os
import random

class Game:

    def __init__(self, max_iters: int = 10) -> None:
        '''
        Game initialization

        Arguments
        ---------
        max_iters (int) - number of questions

        Parameters
        ----------
        self.folder_or_url (str) - URL of the folder with photos
        self.iters (int) - current iter
        self.max_iters (int) - number of questions
        self.mazai_score (int) - number of ML model correct predictions. Now - quantity of user's incorrect answers 
        self.user_score (int) - quantity of user's correct answers 
        self.photo_dataset (list) - list of tuples, there the first value is photo's URL 
                                    and the second value - correct class. 0 - europaeus, 1 - timidus
        self.prediction = [] - ML model predictions. Now empty

        Return
        ------
        None
        '''
        
        self.folder_or_url = 'test_hares_photo/'
        self.iters = 0
        self.max_iters = 10
        self.mazai_score = 0
        self.user_score = 0
        self.photo_dataset = []
        self.prediction = []

    
    def set_difficulty(self, difficulty: str) -> None:
        '''
        Create photo dataset for the current game and make ML model predictions.
        ------------------------------------------------------------------------
        If difficulty == 'Низкий' photo_dataset will contain only photos of lepus europaeus in a winter fur coat,
        lepus europaeus in a summer fur coat, lepus timidus in a winter fur coat, lepus timidus in a summer fur coat.
        If difficulty == 'Средний' photo_dataset will contain only photos of lepus europaeus in a summer fur coat, 
        lepus timidus in a summer fur coat.
        If difficulty == 'Тяжелый' photo_dataset will contain only photos of lepus europaeus in a summer fur coat, 
        lepus europaeus leverets, lepus timidus in a summer fur coat, lepus timidus leverets.
        Each dataset will have at least one photo of each included type.
        After the photo dataset is created, the ML model returns prediction (Now - do not return prediction)

        Arguments
        ---------
        difficulty (str: ['Низкий', 'Средний', 'Высокий']) - level of difficulty for the current game.

        Return
        ------
        None
        '''

        # Save quantity of existing photos
        count_europaeus_leverets = len(os.listdir(self.folder_or_url + 'europaeus_leverets'))
        count_europaeus_summer   = len(os.listdir(self.folder_or_url + 'europaeus_summer'))
        count_europaeus_winter   = len(os.listdir(self.folder_or_url + 'europaeus_winter'))
        count_timidus_leverets   = len(os.listdir(self.folder_or_url + 'timidus_leverets'))
        count_timidus_summer     = len(os.listdir(self.folder_or_url + 'timidus_summer'))
        count_timidus_winter     = len(os.listdir(self.folder_or_url + 'timidus_winter'))

        # Choose one obligatory element for dataset
        europaeus_leverets_photos = [random.randint(1, count_europaeus_leverets)]
        europaeus_summer_photos   = [random.randint(1, count_europaeus_summer)]
        europaeus_winter_photos   = [random.randint(1, count_europaeus_winter)]
        timidus_leverets_photos   = [random.randint(1, count_timidus_leverets)]
        timidus_summer_photos     = [random.randint(1, count_timidus_summer)]
        timidus_winter_photos     = [random.randint(1, count_timidus_winter)]

        # Download other random elements
        if difficulty == 'Низкий':
            europaeus_leverets_photos, timidus_leverets_photos = [], []
            for _ in range(self.max_iters - 4):
                rnd_category = random.randint(0, 3)
                if rnd_category == 0:
                    europaeus_summer_photos.append(random.choice([i for i in range(1, count_europaeus_summer+1) if i not in europaeus_summer_photos]))
                elif rnd_category == 1:
                    timidus_summer_photos.append(random.choice([i for i in range(1, count_timidus_summer+1) if i not in timidus_summer_photos]))
                elif rnd_category == 2:
                    europaeus_winter_photos.append(random.choice([i for i in range(1, count_europaeus_winter+1) if i not in europaeus_winter_photos]))
                else:
                    timidus_winter_photos.append(random.choice([i for i in range(1, count_timidus_winter+1) if i not in timidus_winter_photos]))
            # Here must be ML model for difficulty == 'Низкий'
            # predictions = model.predict(photo_dataset)
            
        elif difficulty == 'Средний':
            europaeus_leverets_photos, europaeus_winter_photos, timidus_leverets_photos, timidus_winter_photos = [], [], [], []
            for _ in range(self.max_iters - 2):
                rnd_category = random.randint(0, 1)
                if rnd_category == 0:
                    europaeus_summer_photos.append(random.choice([i for i in range(1, count_europaeus_summer+1) if i not in europaeus_summer_photos]))
                elif rnd_category == 1:
                    timidus_summer_photos.append(random.choice([i for i in range(1, count_timidus_summer+1) if i not in timidus_summer_photos]))
            # Here must be ML model for difficulty == 'Средний'
            # predictions = model.predict(photo_dataset)

        elif difficulty == 'Тяжелый':
            europaeus_winter_photos, timidus_winter_photos = [], []
            for _ in range(self.max_iters - 4):
                rnd_category = random.randint(0, 3)
                if rnd_category == 0:
                    europaeus_summer_photos.append(random.choice([i for i in range(1, count_europaeus_summer+1) if i not in europaeus_summer_photos]))
                elif rnd_category == 1:
                    timidus_summer_photos.append(random.choice([i for i in range(1, count_timidus_summer+1) if i not in timidus_summer_photos]))
                elif rnd_category == 2:
                    europaeus_leverets_photos.append(random.choice([i for i in range(1, count_europaeus_leverets+1) if i not in europaeus_leverets_photos]))
                else:
                    timidus_leverets_photos.append(random.choice([i for i in range(1, count_timidus_leverets+1) if i not in timidus_leverets_photos]))
            # Here must be ML model for difficulty == 'Тяжелый'
            # predictions = model.predict(photo_dataset)

        # Set labels for the choosen photos
        europaeus_leverets_photos = [(self.folder_or_url + 'europaeus_leverets/' + str(i)+'.jpg', 0) for i in europaeus_leverets_photos]
        europaeus_summer_photos   = [(self.folder_or_url + 'europaeus_summer/' + str(i)+'.jpg', 0) for i in europaeus_summer_photos]
        europaeus_winter_photos   = [(self.folder_or_url + 'europaeus_winter/' + str(i)+'.jpg', 0) for i in europaeus_winter_photos]
        timidus_leverets_photos   = [(self.folder_or_url + 'timidus_leverets/' + str(i)+'.jpg', 1) for i in timidus_leverets_photos]
        timidus_summer_photos     = [(self.folder_or_url + 'timidus_summer/' + str(i)+'.jpg', 1) for i in timidus_summer_photos]
        timidus_winter_photos     = [(self.folder_or_url + 'timidus_winter/' + str(i)+'.jpg', 1) for i in timidus_winter_photos]

        # Create finish dataset and mix elements
        self.photo_dataset = (europaeus_leverets_photos + europaeus_summer_photos + europaeus_winter_photos + 
                              timidus_leverets_photos + timidus_summer_photos + timidus_winter_photos)
        random.shuffle(self.photo_dataset)

        # Make predictions
        # if difficulty == 'Низкий':
        #     # Here must be ML model for difficulty == 'Низкий'
        #     # self.predictions = model.predict([photo for photo, label in self.photo_dataset])
        # elif difficulty == 'Средний':
        #     # Here must be ML model for difficulty == 'Средний'
        #     # self.predictions = model.predict([photo for photo, label in self.photo_dataset])
        # elif difficulty == 'Тяжелый':
        #     # Here must be ML model for difficulty == 'Тяжелый'
        #     # self.predictions = model.predict([photo for photo, label in self.photo_dataset])
    

    def get_iter(self) -> None:
        '''
        Returns current iter

        Return
        ------
        self.iters (int) - current iter 
        '''
        
        return self.iters

    
    def get_curr_photo_url(self) -> str:
        '''
        Returns current iter photo URL

        Return
        ------
        self.photo_dataset[self.iters][0] (str) - URL for photo in photo_dataset for the current iter 
        '''
        
        return self.photo_dataset[self.iters][0]

    
    def check_answer(self, answer: str) -> str:
        '''
        Check if user's answer and model's answer are correct and go on next iter
        -------------------------------------------------------------------------
        If user's answer is correct increment self.user_score. 
        If model's answer is correct increment self.mazai_score (Now - self.mazai_score == 0).

        Arguments
        ---------
        answer (str: ['Русак', 'Беляк']) - user's current answer

        Return
        ------
        Text (str) interpretation of correct answer 
        '''

        if self.iters < self.max_iters:
            if (answer == 'Русак' and self.photo_dataset[self.iters][1] == 0) or (answer == 'Беляк' and self.photo_dataset[self.iters][1] == 1):
                self.user_score += 1
            
            # if (answer == 'Русак' and self.predictions[self.iters] == 0) or (answer == 'Беляк' and self.predictions[self.iters] == 1):
            #     self.mazai_score += 1
            correct_answer = 'Правильный ответ - русак' if self.photo_dataset[self.iters][1] == 0 else 'Правильный ответ - беляк'
            self.iters += 1

            return correct_answer
        

    def get_result(self) -> str:
        '''
        Return text interpretation of user's score and mazai's score (Now - only user's score) 

        Return
        ------
        Text (str) interpretation of user's score and mazai's score (Now - only user's score) 
        '''

        return "{} из {} правильных ответов".format(self.user_score, self.max_iters)
        
        # # Text (str) interpretation of user's score and mazai's score
        # result_text = ''
        # if self.mazai_score == self.user_score:
        #     result_text = ("Всего было {} вопросов. Текущий счет: {}:{}. Ничья! Предлагаю устроить реванш :)"
        #                    .format(self.max_iters, self.mazai_score, self.user_score))
        # elif self.mazai_score < self.user_score:
        #     result_text = ("Всего было {} вопросов. Текущий счет: {}:{}. Счет в твою пользу! MazAI стоит еще немножко подучиться. Но я готов отыграться!"
        #                    .format(self.max_iters, self.mazai_score, self.user_score))
        # else:
        #     result_text = ("Всего было {} вопросов. Текущий счет: {}:{}. Я выиграл :) Но ты всегда можешь отыграться"
        #                    .format(self.max_iters, self.mazai_score, self.user_score))
        # return result_text