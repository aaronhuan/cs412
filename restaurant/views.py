#File: restaurant/views.py
#Author: Aaron Huang (ahuan@bu.edu), 09/16/2025
#Description: Views for the restaurant app handling main, order, and confirmation pages.

import random
from django.shortcuts import render
# Create your views here.

special_items_display = [
    "Dragon Warrior Sized Dumpling $15" ,
    "Furious 5 Toy $7",
    "Sticky Bean Buns $4"
]

special_items = [
    "dragon_warrior_sized_dumpling" ,
    "furious_5_toy",
    "sticky_bean_buns"
]

prices = {
    "noodles": 10,
    "bean_buns": 2,
    "dumplings": 7,
    "almond_cookies": 2,
    "tofu_dessert": 3,
    "dragon_warrior_sized_dumpling": 15,
    "furious_5_toy": 7,
    "sticky_bean_buns": 4,
    "extra_egg": 2,
    "extra_green_onion": 1
}

def main(request):
    """Renders the main page of the restaurant app."""

    return render(request, 'restaurant/main.html')

def order(request):
    """Display the order form with a randomly selected daily special item."""

    # Randomly select a daily special item using random indexing
    special_index = random.randint(0, 2)
    context = {
        "special_items_display": special_items_display[special_index],
        "daily_special_item": special_items[special_index]
    }
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    """Process the form submission and generate a confirmation page of the order."""
    print(request.POST)
    total_price = 0
    selected_items = []
    if request.POST:
        # Process selected items and calculate total price, use .get to avoid KeyError
        noodle = request.POST.get("noodles", 'off')
        if noodle == 'on':
            selected_items.append("Noodles")
            total_price += prices["noodles"]

        extra_egg = request.POST.get("extra_egg", 'off')
        if extra_egg == 'on':
            selected_items.append("Extra Egg")
            total_price += 2
        
        extra_green_onion = request.POST.get("extra_green_onion", 'off')
        if extra_green_onion == 'on':
            selected_items.append("Extra Green Onion")
            total_price += 1
        
        bean_buns = request.POST.get("bean_buns", 'off')
        if bean_buns == 'on':
            selected_items.append("Bean Buns")
            total_price += prices["bean_buns"]

        dumplings = request.POST.get("dumplings", 'off')
        if dumplings == 'on':  
            selected_items.append("Dumplings")
            total_price += prices["dumplings"]
        
        almond_cookies = request.POST.get("almond_cookies", 'off')
        if almond_cookies == 'on':
            selected_items.append("Almond Cookies")
            total_price += prices["almond_cookies"]
        
        tofu_dessert = request.POST.get("tofu_dessert", 'off')
        if tofu_dessert == 'on':
            selected_items.append("Tofu Dessert")
            total_price += prices["tofu_dessert"]

        is_dragon_dumpling = request.POST.get("dragon_warrior_sized_dumpling", 'off')
        if is_dragon_dumpling == 'on':
            selected_items.append("Dragon Warrior Sized Dumpling")
            total_price += prices["dragon_warrior_sized_dumpling"]
        
        is_furious_5_toy = request.POST.get("furious_5_toy", 'off')
        if is_furious_5_toy == 'on':
            selected_items.append("Furious 5 Toy")
            total_price += prices["furious_5_toy"]

        is_sticky_bean_buns = request.POST.get("sticky_bean_buns", 'off')
        if is_sticky_bean_buns == 'on':    
            selected_items.append("Sticky Bean Buns")
            total_price += prices["sticky_bean_buns"]

        name = request.POST.get("name", "")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        special_instructions = request.POST["special_instructions"]

        context = {
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "special_instructions": special_instructions,
            "ordered_items": selected_items,
            "total_price": total_price
        }

    return render(request, 'restaurant/confirmation.html', context)
