from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'bmr' in request.form:  # 檢查是否提交了手動填寫的BMR
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

            protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content = suggest_foods(protein_min, protein_max, fat_min, fat_max, carbs)


            return render_template('result_manual.html',bmr=bmr , tdee=tdee, total_calories=total_calories, protein_min=protein_min
            , protein_max=protein_max, fat_min=fat_min, fat_max=fat_max, carbs=carbs, protein_foods=protein_foods, fat_foods=fat_foods, carb_foods=carb_foods,
            protein_content=protein_content, fat_content=fat_content, carb_content=carb_content)

        else:  # 計算BMR的表單
            gender = request.form['gender']
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            age = int(request.form['age'])

            bmr = calculate_bmr(gender, height, weight, age)
            
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

            protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content = suggest_foods(protein_min, protein_max, fat_min, fat_max, carbs)


            return render_template('result_manual.html',bmr=bmr , tdee=tdee, total_calories=total_calories, protein_min=protein_min
            , protein_max=protein_max, fat_min=fat_min, fat_max=fat_max, carbs=carbs, protein_foods=protein_foods, fat_foods=fat_foods, carb_foods=carb_foods,
            protein_content=protein_content, fat_content=fat_content, carb_content=carb_content)

    return render_template('index.html')

def calculate_bmr(gender, height, weight, age):
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

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

def suggest_foods(protein_min, protein_max, fat_min, fat_max, carbs):
    # 建議每日攝取的蛋白質
    protein_suggestion = (protein_min + protein_max) / 2

    # 建議每日攝取的脂肪
    fat_suggestion = (fat_min + fat_max) / 2

    # 建議每日攝取的碳水化合物
    carbs_suggestion = carbs

     # 食物的營養素含量
    protein_content = {
        '雞胸肉': 30,  # 雞胸肉每100g含有約30g蛋白質
        '鮭魚': 20,    # 牛肉每100g含有約25g蛋白質
        '牛肉': 26,    # 鮭魚每100g含有約22g蛋白質
        '乳清蛋白粉': 23,  # 蛋白粉每份含有約23g蛋白質
    }

    fat_content = {
        '堅果': 5,        # 堅果每10g含有約5g脂肪
        '橄欖油': 10,    # 橄欖油每10g含有約10g脂肪
    }

    carb_content = {
        '白米': 29,     # 白米每100g含有約30g碳水化合物
        '燕麥': 60,   # 燕麥片每100g含有約60g碳水化合物
        '地瓜': 23,
        '馬鈴薯': 18,   # 馬鈴薯每100g含有約20g碳水化合物
    }

    # 建議的食物品項和份量
    protein_foods = {
        '雞胸肉': round(protein_suggestion / 30),  # 雞胸肉每100g含有約30g蛋白質
        '鮭魚': round(protein_suggestion / 20),    # 鮭魚每100g含有約20g蛋白質
        '牛肉': round(protein_suggestion / 26),    # 牛肉每100g含有約26g蛋白質
        '乳清蛋白粉': round(protein_suggestion / 23) # 蛋白粉每份含有約23g蛋白質 
    }

    fat_foods = {
        '堅果': round(fat_suggestion / 5.5),        # 堅果每100g含有約55g脂肪
        '橄欖油': round(fat_suggestion / 10)      # 橄欖油每100g含有約100g脂肪
    }

    carb_foods = {
        '白米': round(carbs_suggestion / 29),     # 白米每100g含有約29g碳水化合物
        '燕麥': round(carbs_suggestion / 60),     # 燕麥每100g含有約60g碳水化合物
        '地瓜': round(carbs_suggestion / 23),     # 地瓜每100g含有約23g碳水化合物
        '馬鈴薯': round(carbs_suggestion / 18)    # 馬鈴薯每100g含有約18g碳水化合物
    }

    return protein_foods, fat_foods, carb_foods, protein_content, fat_content, carb_content


if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5000))

