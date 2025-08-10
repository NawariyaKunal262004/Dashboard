import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

def run_grocery_manager():
    """Run the grocery manager tool"""
    st.markdown("## �� Grocery Manager")
    
    # Initialize session state
    if 'grocery_list' not in st.session_state:
        st.session_state.grocery_list = []
    
    if 'grocery_history' not in st.session_state:
        st.session_state.grocery_history = []
    
    if 'shopping_lists' not in st.session_state:
        st.session_state.shopping_lists = []
    
    if 'budget' not in st.session_state:
        st.session_state.budget = {"monthly": 500, "spent": 0, "remaining": 500}
    
    if 'recipes' not in st.session_state:
        st.session_state.recipes = []
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Choose a section:",
            ["📝 Shopping List", "💰 Budget Tracker", "📋 Recipe Manager", "📊 Analytics", "⚙️ Settings"]
        )
    
    if page == "📝 Shopping List":
        show_shopping_list()
    elif page == "💰 Budget Tracker":
        show_budget_tracker()
    elif page == "📋 Recipe Manager":
        show_recipe_manager()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def show_shopping_list():
    """Show the main shopping list interface"""
    st.markdown("### 📝 Shopping List")
    
    # Add new item section
    with st.expander("➕ Add New Item", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            item_name = st.text_input("Item Name", key="new_item_name")
            category = st.selectbox("Category", [
                "Fruits & Vegetables", "Dairy & Eggs", "Meat & Fish", 
                "Grains & Bread", "Snacks & Beverages", "Frozen Foods",
                "Canned Goods", "Condiments", "Household", "Other"
            ], key="new_item_category")
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0.1, value=1.0, step=0.1, key="new_item_qty")
            unit = st.selectbox("Unit", ["pcs", "kg", "g", "l", "ml", "pack", "bottle", "can"], key="new_item_unit")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"], key="new_item_priority")
        
        with col3:
            estimated_price = st.number_input("Estimated Price ($)", min_value=0.0, value=0.0, step=0.01, key="new_item_price")
            store = st.selectbox("Preferred Store", ["Any", "Walmart", "Target", "Kroger", "Whole Foods", "Local Market"], key="new_item_store")
        
        if st.button("➕ Add Item", use_container_width=True):
            if item_name:
                new_item = {
                    "id": len(st.session_state.grocery_list) + 1,
                    "name": item_name,
                    "quantity": quantity,
                    "unit": unit,
                    "category": category,
                    "priority": priority,
                    "estimated_price": estimated_price,
                    "store": store,
                    "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "completed": False,
                    "notes": ""
                }
                st.session_state.grocery_list.append(new_item)
                st.success(f"✅ Added {item_name} to your shopping list!")
                st.rerun()
    
    # Current list display
    if not st.session_state.grocery_list:
        st.info("🛒 Your shopping list is empty. Add some items to get started!")
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_category = st.selectbox("Filter by Category", ["All"] + list(set([item["category"] for item in st.session_state.grocery_list])))
        with col2:
            filter_priority = st.selectbox("Filter by Priority", ["All", "Low", "Medium", "High", "Urgent"])
        with col3:
            filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        
        # Apply filters
        filtered_items = st.session_state.grocery_list
        if filter_category != "All":
            filtered_items = [item for item in filtered_items if item["category"] == filter_category]
        if filter_priority != "All":
            filtered_items = [item for item in filtered_items if item["priority"] == filter_priority]
        if filter_status == "Pending":
            filtered_items = [item for item in filtered_items if not item["completed"]]
        elif filter_status == "Completed":
            filtered_items = [item for item in filtered_items if item["completed"]]
        
        # Group by category
        categories = {}
        for item in filtered_items:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        # Display items
        for category, items in categories.items():
            with st.expander(f"🛒 {category} ({len(items)} items)", expanded=True):
                for i, item in enumerate(items):
                    with st.container():
                        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**{item['name']}**")
                            if item['notes']:
                                st.caption(f"📝 {item['notes']}")
                            st.caption(f"Added: {item['added_date']}")
                        
                        with col2:
                            st.write(f"{item['quantity']} {item['unit']}")
                        
                        with col3:
                            priority_colors = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}
                            st.write(f"{priority_colors[item['priority']]} {item['priority']}")
                        
                        with col4:
                            if item['estimated_price'] > 0:
                                st.write(f"${item['estimated_price']:.2f}")
                            else:
                                st.write("$--")
                        
                        with col5:
                            if not item["completed"]:
                                if st.button("✅", key=f"complete_{item['id']}"):
                                    item["completed"] = True
                                    item["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                    st.session_state.grocery_history.append(item.copy())
                                    st.session_state.budget["spent"] += item["estimated_price"]
                                    st.session_state.budget["remaining"] = st.session_state.budget["monthly"] - st.session_state.budget["spent"]
                                    st.rerun()
                            else:
                                st.write("✅")
                        
                        # Item actions
                        with st.expander("Actions", expanded=False):
                            col_a1, col_a2, col_a3 = st.columns(3)
                            with col_a1:
                                if st.button("✏️ Edit", key=f"edit_{item['id']}"):
                                    st.session_state.editing_item = item['id']
                                    st.rerun()
                            with col_a2:
                                if st.button("🗑️ Delete", key=f"delete_{item['id']}"):
                                    st.session_state.grocery_list.remove(item)
                                    st.rerun()
                            with col_a3:
                                notes = st.text_input("Notes", value=item.get("notes", ""), key=f"notes_{item['id']}")
                                if notes != item.get("notes", ""):
                                    item["notes"] = notes

def show_budget_tracker():
    """Show budget tracking interface"""
    st.markdown("### 💰 Budget Tracker")
    
    # Budget overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Budget", f"${st.session_state.budget['monthly']:.2f}")
    
    with col2:
        st.metric("Spent", f"${st.session_state.budget['spent']:.2f}")
    
    with col3:
        st.metric("Remaining", f"${st.session_state.budget['remaining']:.2f}")
    
    with col4:
        if st.session_state.budget['monthly'] > 0:
            progress = st.session_state.budget['spent'] / st.session_state.budget['monthly']
            st.metric("Progress", f"{progress:.1%}")
        else:
            st.metric("Progress", "0%")
    
    # Budget progress bar
    if st.session_state.budget['monthly'] > 0:
        progress = st.session_state.budget['spent'] / st.session_state.budget['monthly']
        st.progress(progress)
        
        if progress > 0.9:
            st.warning("⚠️ You're approaching your monthly budget limit!")
        elif progress > 0.7:
            st.info("ℹ️ You've used 70% of your monthly budget.")
    
    # Budget settings
    with st.expander("⚙️ Budget Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_budget = st.number_input("Monthly Budget ($)", min_value=0, value=int(st.session_state.budget['monthly']), step=50)
        with col2:
            if st.button("Update Budget"):
                st.session_state.budget['monthly'] = new_budget
                st.session_state.budget['remaining'] = new_budget - st.session_state.budget['spent']
                st.success("Budget updated successfully!")
                st.rerun()
    
    # Spending history
    st.markdown("### 📊 Spending History")
    
    if st.session_state.grocery_history:
        # Create spending data
        spending_data = []
        for item in st.session_state.grocery_history:
            if item.get("completed_date") and item.get("estimated_price", 0) > 0:
                spending_data.append({
                    "date": item["completed_date"][:10],
                    "item": item["name"],
                    "amount": item["estimated_price"],
                    "category": item["category"]
                })
        
        if spending_data:
            df = pd.DataFrame(spending_data)
            df['date'] = pd.to_datetime(df['date'])
            
            # Group by date
            daily_spending = df.groupby('date')['amount'].sum().reset_index()
            
            # Display chart
            st.line_chart(daily_spending.set_index('date'))
            
            # Recent transactions
            st.markdown("#### Recent Transactions")
            recent_transactions = df.tail(10)
            for _, row in recent_transactions.iterrows():
                st.write(f"📅 {row['date'].strftime('%Y-%m-%d')} - {row['item']} (${row['amount']:.2f})")
    else:
        st.info("No spending history available yet.")

def show_recipe_manager():
    """Show recipe management interface"""
    st.markdown("### 📋 Recipe Manager")
    
    # Add new recipe
    with st.expander("➕ Add New Recipe", expanded=False):
        recipe_name = st.text_input("Recipe Name")
        recipe_description = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            prep_time = st.number_input("Prep Time (minutes)", min_value=0, value=30)
            cook_time = st.number_input("Cook Time (minutes)", min_value=0, value=45)
        with col2:
            servings = st.number_input("Servings", min_value=1, value=4)
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        
        # Ingredients
        st.markdown("#### Ingredients")
        ingredients = []
        for i in range(5):
            col1, col2, col3 = st.columns(3)
            with col1:
                ingredient = st.text_input(f"Ingredient {i+1}", key=f"ingredient_{i}")
            with col2:
                amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1, key=f"amount_{i}")
            with col3:
                unit = st.selectbox("Unit", ["pcs", "kg", "g", "l", "ml", "cup", "tbsp", "tsp"], key=f"unit_{i}")
            
            if ingredient:
                ingredients.append({"name": ingredient, "amount": amount, "unit": unit})
        
        if st.button("Save Recipe"):
            if recipe_name:
                new_recipe = {
                    "id": len(st.session_state.recipes) + 1,
                    "name": recipe_name,
                    "description": recipe_description,
                    "prep_time": prep_time,
                    "cook_time": cook_time,
                    "servings": servings,
                    "difficulty": difficulty,
                    "ingredients": ingredients,
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.recipes.append(new_recipe)
                st.success(f"✅ Recipe '{recipe_name}' saved successfully!")
                st.rerun()
    
    # Display recipes
    if st.session_state.recipes:
        st.markdown("#### Saved Recipes")
        for recipe in st.session_state.recipes:
            with st.expander(f"🍳 {recipe['name']} ({recipe['difficulty']})", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {recipe['description']}")
                    st.write(f"**Prep Time:** {recipe['prep_time']} min | **Cook Time:** {recipe['cook_time']} min | **Servings:** {recipe['servings']}")
                    
                    st.markdown("**Ingredients:**")
                    for ingredient in recipe['ingredients']:
                        st.write(f"• {ingredient['amount']} {ingredient['unit']} {ingredient['name']}")
                
                with col2:
                    if st.button("🛒 Add to Shopping List", key=f"add_recipe_{recipe['id']}"):
                        for ingredient in recipe['ingredients']:
                            new_item = {
                                "id": len(st.session_state.grocery_list) + 1,
                                "name": ingredient['name'],
                                "quantity": ingredient['amount'],
                                "unit": ingredient['unit'],
                                "category": "Other",
                                "priority": "Medium",
                                "estimated_price": 0.0,
                                "store": "Any",
                                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "completed": False,
                                "notes": f"From recipe: {recipe['name']}"
                            }
                            st.session_state.grocery_list.append(new_item)
                        st.success(f"✅ Added all ingredients from '{recipe['name']}' to shopping list!")
                        st.rerun()
    else:
        st.info("No recipes saved yet. Add your first recipe!")

def show_analytics():
    """Show analytics and insights"""
    st.markdown("### 📊 Analytics & Insights")
    
    if not st.session_state.grocery_list and not st.session_state.grocery_history:
        st.info("No data available for analytics yet. Start adding items to your shopping list!")
        return
    
    # Basic statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(st.session_state.grocery_list)
        st.metric("Total Items", total_items)
    
    with col2:
        completed_items = len([item for item in st.session_state.grocery_list if item["completed"]])
        st.metric("Completed Items", completed_items)
    
    with col3:
        pending_items = total_items - completed_items
        st.metric("Pending Items", pending_items)
    
    with col4:
        if total_items > 0:
            completion_rate = completed_items / total_items
            st.metric("Completion Rate", f"{completion_rate:.1%}")
        else:
            st.metric("Completion Rate", "0%")
    
    # Category analysis
    if st.session_state.grocery_list:
        st.markdown("#### 📈 Category Analysis")
        
        category_counts = {}
        for item in st.session_state.grocery_list:
            cat = item["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            # Create bar chart
            categories = list(category_counts.keys())
            counts = list(category_counts.values())
            
            chart_data = pd.DataFrame({
                'Category': categories,
                'Count': counts
            })
            
            st.bar_chart(chart_data.set_index('Category'))
    
    # Priority analysis
    if st.session_state.grocery_list:
        st.markdown("#### 🎯 Priority Analysis")
        
        priority_counts = {}
        for item in st.session_state.grocery_list:
            priority = item["priority"]
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        if priority_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Priority Distribution:**")
                for priority, count in priority_counts.items():
                    st.write(f"• {priority}: {count} items")
            
            with col2:
                # Priority pie chart
                priority_data = pd.DataFrame({
                    'Priority': list(priority_counts.keys()),
                    'Count': list(priority_counts.values())
                })
                
                st.bar_chart(priority_data.set_index('Priority'))

def show_settings():
    """Show settings interface"""
    st.markdown("### ⚙️ Settings")
    
    # General settings
    st.markdown("#### General Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_store = st.selectbox("Default Store", ["Any", "Walmart", "Target", "Kroger", "Whole Foods", "Local Market"])
        default_currency = st.selectbox("Default Currency", ["USD", "EUR", "GBP", "CAD", "AUD"])
    
    with col2:
        notifications = st.checkbox("Enable Notifications", value=True)
        auto_save = st.checkbox("Auto-save Changes", value=True)
    
    # Data management
    st.markdown("#### Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Data", use_container_width=True):
            # Export functionality would go here
            st.info("Export functionality would save your data to a JSON file.")
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.checkbox("I understand this will delete all my data"):
                st.session_state.grocery_list = []
                st.session_state.grocery_history = []
                st.session_state.shopping_lists = []
                st.session_state.budget = {"monthly": 500, "spent": 0, "remaining": 500}
                st.session_state.recipes = []
                st.success("All data cleared successfully!")
                st.rerun()
    
    # About
    st.markdown("#### About")
    st.write("**Grocery Manager v2.0**")
    st.write("A comprehensive grocery management tool built with Streamlit.")
    st.write("Features include shopping lists, budget tracking, recipe management, and analytics.")
