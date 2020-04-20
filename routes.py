from config import app
from controller import index, add_user, about, price, user_page, login, logout, schedule, process_schedule, confirm, delete_pickup, edit_pickup, update_pickup, edit_address, update_address, edit_user, update_user


app.add_url_rule("/", view_func=index)
app.add_url_rule("/process/user", view_func=add_user, methods=['POST'])
app.add_url_rule("/about", view_func=about)
app.add_url_rule("/price", view_func=price)
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/user_page", view_func=user_page)
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/schedule", view_func=schedule)
app.add_url_rule("/process/schedule", view_func=process_schedule, methods=['POST'])
app.add_url_rule("/confirmation", view_func=confirm)
app.add_url_rule("/delete/<schedule_id>", view_func=delete_pickup)
app.add_url_rule("/edit/schedule", view_func=edit_pickup)
app.add_url_rule("/update/schedule/<schedule_id>", view_func=update_pickup, methods=['POST'])
app.add_url_rule("/edit/address", view_func=edit_address)
app.add_url_rule("/update/address/<address_id>", view_func=update_address, methods=['POST'])
app.add_url_rule("/edit/user", view_func=edit_user)
app.add_url_rule("/update/user/<user_id>", view_func=update_user, methods=['POST'])
