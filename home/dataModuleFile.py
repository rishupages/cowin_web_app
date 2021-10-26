from datetime import date


# class Age CheckUp:
#     # is_2 = False
#     # is_12 = False
#     # is_18 = False
#     # is_45 = False
#     # is_60 = False

#     def check_Age_Category(self, yob):
#         # age = 2021 - yob
#         # if age > 2 <= 12:
#         #     self.is_2 = True
#         #     return self.is_2
#         # elif age > 12 <= 18:
#         #     self.is_12 = True
#         #     return self.is_12
#         # elif age > 18 <= 45:
#         #     self.is_18 = True
#         #     return self.is_48
#         # elif age > 45 <= 60:
#         #     self.is_45 = True
#         #     return self.is_45
#         # elif age > 60:
#         #     self.is_60 = True
#         #     return self.is_60


class UserAgeCheckClass:
    def age_calculate(self, yob):
        currentDate = date.today()
        currentYear = currentDate.year
        age = currentYear-yob
        return age
