from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "secrecy123"

# Расширенная база данных автомобилей
CARS_DATABASE = [
    {
        "id": 1,
        "brand": "kia",
        "brand_name": "Kia",
        "model": "Rio",
        "year": 2019,
        "body": "sedan",
        "body_name": "Седан",
        "price": 1200000,
        "mileage": "85 000 км",
        "engine": "1.6 л / 123 л.с.",
        "transmission": "Автомат",
        "image": "https://s.auto.drom.ru/i24247/r/photos/1416074/big_1517568.jpg"
    },
    {
        "id": 2,
        "brand": "kia",
        "brand_name": "Kia",
        "model": "Sportage",
        "year": 2020,
        "body": "suv",
        "body_name": "Внедорожник",
        "price": 2300000,
        "mileage": "62 000 км",
        "engine": "2.0 л / 150 л.с.",
        "transmission": "Автомат",
        "image": "https://s.auto.drom.ru/i24246/r/photos/1414943/big_1511648.jpg"
    },
    {
        "id": 3,
        "brand": "hyundai",
        "brand_name": "Hyundai",
        "model": "Solaris",
        "year": 2018,
        "body": "sedan",
        "body_name": "Седан",
        "price": 1150000,
        "mileage": "98 000 км",
        "engine": "1.6 л / 123 л.с.",
        "transmission": "Механика",
        "image": "https://image.rdm-import.ru/wp-E3Vi1WS_CszbRfeZND-iaGh5WFlh5xs_-R1jMCMI/w:0/h:0/rt:fit/g:ce:0:0/aHR0cHM6Ly9zdG9yYWdlLnlhbmRleGNsb3VkLm5ldC9yZG0taW1wb3J0LWltYWdlcy9wcm9kdWN0LzM5NDE3L2h0dHBzcmRtLWltcG9ydCAzOTQxNyDQutC-0L_QuNGPIC5qcGc.jpg"
    },
    {
        "id": 4,
        "brand": "toyota",
        "brand_name": "Toyota",
        "model": "RAV4",
        "year": 2021,
        "body": "suv",
        "body_name": "Внедорожник",
        "price": 3100000,
        "mileage": "45 000 км",
        "engine": "2.0 л / 149 л.с.",
        "transmission": "Вариатор",
        "image": "https://s.auto.drom.ru/i24255/r/photos/1423597/big_1552669.jpg"
    },
    {
        "id": 5,
        "brand": "volkswagen",
        "brand_name": "Volkswagen",
        "model": "Golf",
        "year": 2017,
        "body": "hatchback",
        "body_name": "Хэтчбек",
        "price": 1400000,
        "mileage": "110 000 км",
        "engine": "1.4 л / 125 л.с.",
        "transmission": "Робот (DSG)",
        "image": "https://s.auto.drom.ru/i24302/r/photos/1453345/big_1700395.jpg"
    },
]

def filter_cars(brand, body, price_max):
    """Общая функция фильтрации автомобилей."""
    filtered = CARS_DATABASE

    if brand:
        filtered = [car for car in filtered if car["brand"] == brand]

    if body:
        filtered = [car for car in filtered if car["body"] == body]

    if price_max:
        try:
            price_limit = int(price_max)
            filtered = [car for car in filtered if car["price"] <= price_limit]
        except ValueError:
            pass

    # Добавляем красиво отформатированную цену (например: 1 200 000)
    for car in filtered:
        car["formatted_price"] = f"{car['price']:,}".replace(",", " ")

    return filtered

@app.route("/", methods=["GET"])
def index():
    """Главная страница с быстрым фильтром."""
    selected_brand = request.args.get("brand", "").strip()
    selected_body = request.args.get("body", "").strip()
    price_max = request.args.get("price_max", "").strip()

    filtered_cars = filter_cars(selected_brand, selected_body, price_max)

    return render_template(
        "index.html",
        cars_count=len(filtered_cars),
        brand=selected_brand,
        body=selected_body,
        price_max=price_max
    )

@app.route("/catalog", methods=["GET"])
def catalog():
    """Страница каталога со списком найденных авто."""
    selected_brand = request.args.get("brand", "").strip()
    selected_body = request.args.get("body", "").strip()
    price_max = request.args.get("price_max", "").strip()

    filtered_cars = CARS_DATABASE
    if selected_brand:
        filtered_cars=[car for car in filtered_cars if car["brand"] == selected_brand]
    if selected_body:
        filtered_cars=[car for car in filtered_cars if car["body"] == selected_body]
    if price_max:
        try:
            price_limit=int(price_max)
            filtered_cars=[car for car in filtered_cars if car["price"] <= price_limit]
        except ValueError:
            pass
    fav_ids=session.get("favorites", [])
    for car in filtered_cars:
        car["formatted_price"] = f"{car['price']:,}".replace(",", " ")
        car["is_favorite"] = car["id"] in fav_ids

    return render_template(
        "catalog.html",
        cars=filtered_cars,
        cars_count=len(filtered_cars),
        brand=selected_brand,
        body=selected_body,
        price_max=price_max
    )
@app.route("/toggle-favorite/<int:car_id>", methods=["POST"])
def toggle_favorite(car_id):
    if "favorites" not in session:
        session["favorites"] = []
    favs=list(session["favorites"])
    if car_id in favs:
        favs.remove(car_id)
        is_fav=False
    else:
        favs.append(car_id)
        is_fav=True
    session["favorites"]=favs
    return jsonify({"success": True, "is_favorite": is_fav, "count": len(favs)})
@app.route("/favorites", methods=["GET"])
def favorites():
    fav_ids=session.get("favorites", [])
    fav_cars=[car for car in CARS_DATABASE if car["id"] in fav_ids]
    for car in fav_cars:
        car["formatted_price"] = f"{car['price']:,}".replace(",", " ")
        car["is_favorite"] = True
    return render_template("favorites.html", cars=fav_cars)

if __name__ == "__main__":
    app.run(debug=True)
