from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        bmr = float(request.form['bmr'])
        activity_level = request.form['activity_level']
        experience = request.form['experience']
        goal = request.form['goal']
        weight = float(request.form['weight'])  # 轉換為浮點數

        tdee = calculate_tdee(bmr, activity_level)
        total_calories = calculate_total_calories(tdee, goal, experience)
        protein_min, protein_max, fat_min, fat_max, carbs = calculate_macronutrients(total_calories, weight, goal)

        # 將浮點數轉換為整數
        tdee = int(tdee)
        total_calories = int(total_calories)
        protein_min = int(protein_min)
        protein_max = int(protein_max)
        fat_min = int(fat_min)
        fat_max = int(fat_max)
        carbs = int(carbs)

        return render_template('result.html', tdee=tdee, total_calories=total_calories, protein_min=protein_min, protein_max=protein_max, fat_min=fat_min, fat_max=fat_max, carbs=carbs)

    return render_template('index.html')

def calculate_tdee(bmr, activity_level):
    if activity_level == 'sedentary':
        activity_factor = 1.2
    elif activity_level == 'lightly active':
        activity_factor = 1.375
    elif activity_level == 'moderately active':
        activity_factor = 1.55
    elif activity_level == 'very active':
        activity_factor = 1.725
    elif activity_level == 'extremely active':
        activity_factor = 1.9
    else:
        raise ValueError("Invalid activity level")

    tdee = bmr * activity_factor
    return tdee

def calculate_total_calories(tdee, goal, experience):
    if experience == '新手':
        if goal == '增肌':
            total_calories = tdee + 100  # 新手增肌目標，每天多攝取100卡路里
        elif goal == '減脂':
            total_calories = tdee - 200  # 新手減脂目標，每天少攝取200卡路里
        else:
            raise ValueError("Invalid goal")
    elif experience == '老手':
        if goal == '增肌':
            total_calories = tdee + 300  # 老手增肌目標，每天多攝取300卡路里
        elif goal == '減脂':
            total_calories = tdee - 400  # 老手減脂目標，每天少攝取400卡路里
        else:
            raise ValueError("Invalid goal")
    else:
        raise ValueError("Invalid experience")
    
    return total_calories

def calculate_macronutrients(total_calories, weight, goal):
    # 計算蛋白質建議攝取量
    if goal == '增肌':
        protein_min = weight * 1.6
        protein_max = weight * 2.2
    elif goal == '減脂':
        protein_min = weight * 2.2
        protein_max = weight * 2.5
    else:
        raise ValueError("Invalid goal")
    
    # 計算脂肪建議攝取量
    fat_min = weight * 0.8
    fat_max = weight * 1
    
    # 計算剩餘熱量分配給碳水化合物
    remaining_calories = total_calories - ((protein_min+protein_max)/2 * 4) - ((fat_min+fat_max)/2 * 9)
    carbs = remaining_calories / 4
    
    return protein_min, protein_max, fat_min, fat_max, carbs

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5000))

