# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect, url_for, flash, session, json
from jinja2  import TemplateNotFound
from datetime import datetime
from flask import jsonify
# App modules
from app import app, dbConn, cursor

# from app.models import Profiles

#Test
@app.route('/productstest')
def getproductss():
    sql = "select * from Products"
    cursor.execute(sql)
    products= cursor.fetchall()
    return render_template('ProductsTest.html', products=products)
   


# App main route + generic routing
@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def loginpage():
    return render_template('Login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Step 1: retrieve user login based on slider type 
    slider = request.form.get('slider')
    if slider == 'Manager':
        c_email = request.form.get('c-email')
        c_psw = request.form.get('c-psw')
        # check if information exists in database
        sql = 'SELECT * FROM Users WHERE Username = %s AND Password = %s AND UserType = %s'
        cursor.execute(sql, [c_email, c_psw, slider])
        find_user = cursor.fetchall()
        error = False
        if not find_user:
            error = True
            flash('We could not find your account. Please try again')
            return render_template('Login.html', c_email=c_email, c_psw=c_psw)
        else:
            for user in find_user:
                 session['user'] = user
                 return render_template('WelcomeManager.html', find_user=find_user)
            # else:
            #     # If the user is not found in the fetched rows, display an error message
            #     flash('We could not find your account. Please try again')
            #     return render_template('Login.html', c_email=c_email, c_psw=c_psw)
        
    # If user is an inverstigator
    elif slider == 'Investigator':
        m_email = request.form.get('m-email')
        m_psw = request.form.get('m-psw')
        # check if information exists in database
        sql = 'SELECT * FROM Users WHERE Username = %s AND Password = %s AND UserType = %s'
        cursor.execute(sql, [m_email, m_psw, slider])
        find_user = cursor.fetchall()
        error = False
        if not find_user:
            error = True
            flash('Invalid Login')
            return render_template('Login.html', m_email=m_email, m_psw=m_psw)
        else:
            for user in find_user:
                session['user'] = user
                return render_template('WelcomeInvestigator.html', find_user=find_user)
            # else:
            #     # If the user is not found in the fetched rows, display an error message
            #     flash('User not found')
            #     return render_template('Login.html', m_email=m_email, m_psw=m_psw)           
    else:
        #flash('Please enter an email and password')
        return render_template('Login.html')



@app.route('/welcomeinvestigator')
def welcomeinvestigator():
    return render_template('WelcomeInvestigator.html')


@app.route('/welcomemanager')
def welcomemanager():
    return render_template('WelcomeManager.html')

@app.route('/reports')
def reports():
    return render_template('RecallReports.html')



#Add product to recall
@app.route('/addproduct')
def addproduct():
    return render_template('AddProduct.html')

@app.route('/newproduct', methods=['POST', 'GET'])
def newproduct():
    if request.method == 'POST':
        pname = request.form.get('pname')
        type = request.form.get('type')
        description = request.form.get('description')
        modelnumber = request.form.get('modelnumber')
        manufacturer = request.form.get('manufacturer')
        pid = request.form.get('pid')
        error = False
        if not pname:
            error = True
            flash("Please provide a Product Name!")
        
        if type == "":
            error = True
            flash("Please provide a Product Type!")
        
        if not description:
            error = True
            flash("Please provide a Description!")

        if not modelnumber:
            error = True
            flash("Please provide a Model Number!")

        if not manufacturer:
            error = True
            flash("Please provide a Manufacturer!")

        if not error:
            
        # if rid is empty, add a new recall to the database
            if not pid: 
                sql = "INSERT INTO Products(ProductName, Description, ModelNumber, Manufacturer, ProductType) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (pname, description, modelnumber, manufacturer, type)) 
                cursor.execute("SELECT * FROM Products")
                products = cursor.fetchall()
                dbConn.commit()
                flash("New product has been added!")
                return render_template('AddRecalls.html', products=products)
            else:
                sql = "INSERT INTO Products(ProductName, Description, ModelNumber, Manufacturer, ProductType, ProductID) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (pname, description, modelnumber, manufacturer, type, pid)) 
                cursor.execute("SELECT * FROM Products")
                products = cursor.fetchall()
                dbConn.commit()
                flash("New product has been added!")
            return render_template('AddRecalls.html', products=products) 
        else:   
            return render_template('AddProduct.html', pname=pname, description=description, modelnumber=modelnumber, manufacturer=manufacturer, type=type)
    else:
        return render_template('AddProduct.html')

@app.route('/recalls')
def recalls():
    sql = "select * from Recalls"
    cursor.execute(sql)
    recall= cursor.fetchall()
    return render_template('Recalls.html', recall=recall)
    

@app.route('/addhighpriority')
def addhighpriority():
    cursor.execute("SELECT * FROM Recalls")
    Recalls = cursor.fetchall()
    return render_template('AddHighPriorityTable.html', Recalls=Recalls)

@app.route('/addhighpriorityinput')
def addhighpriorityinput():
    return render_template('AddHighPriorityInput.html')

@app.route('/highpriority')
def highpriority():
    sql = "select * from Priority"
    cursor.execute(sql)
    priority= cursor.fetchall()
    return render_template('HighPriority.html', priority=priority)

@app.route('/addrecalls')
def addrecalls():
    sql = "select * from Products"
    cursor.execute(sql)
    products= cursor.fetchall()
    return render_template('AddRecalls.html', products=products)
    

# add product to Recalls Table
@app.route('/addRecall', methods=['POST', 'GET'])
def addRecall():  
    if request.method == 'POST':
        rid = request.form.get('rid')
        type = request.form.get("type")
        recalldatetime = datetime.now()
        recallnumber = request.form.get('recallnumber')
        remedy = request.form.get('remedy')
        pname = request.form.get('pname')
        title = request.form.get('title')
        reason = request.form.get('reason')
        
        #input validation
        error = False
        if not pname:
            error = True
            flash("Please provide a Product Name!")
        
        if type == "":
            error = True
            flash("Please provide a Recall Type!")

        if not recallnumber:
            error = True
            flash("Please provide a Recall Number!")

        if not remedy:
            error = True
            flash("Please provide a Remedy!")
            
        if not title:
            error = True
            flash("Please provide a Recall Title!")

        if not reason:
            error = True
            flash("Please provide a Recall Reason!")
        
        
        if not error:
            
        # if rid is empty, add a new recall to the database
            if not rid: 
                sql = "INSERT INTO Recalls(RecallType, RecallDateTime, RecallNumber, RecallRemedy, ProductID, RecallTitle, RecallReason) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (type, recalldatetime, recallnumber, remedy, pname, title ,reason)) 
                cursor.execute("SELECT * FROM Recalls")
                recall = cursor.fetchall()
                dbConn.commit()
                flash("New recall has been added!")
                return render_template('Recalls.html', recall=recall)
            else:
                sql = "INSERT INTO Recalls(RecallType, RecallDateTime, RecallNumber, RecallRemedy, RecallID,  ProductID, RecallTitle, RecallReason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (type, recalldatetime,recallnumber, remedy, rid,  pname, title, reason))
                cursor.execute("SELECT * FROM Recalls")
                recall = cursor.fetchall()
                dbConn.commit()
                flash("New recall has been added!")
                return render_template('Recalls.html', recall=recall) 

        else:
            cursor.execute("SELECT * FROM Products")
            products = cursor.fetchall()
            return render_template('AddRecalls.html', rid=rid, type=type, recalldatetime=recalldatetime, recallnumber=recallnumber, remedy=remedy, pname=pname, products=products, title=title, reason=reason)
    else:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return render_template('AddRecalls.html', rid=rid, type=type, recalldatetime=recalldatetime, recallnumber=recallnumber, remedy=remedy, pname=pname, products=products, title=title, reason=reason)




#Add to high priority
@app.route('/addhighpriority1', methods=['POST', 'GET'])
def addHighPriority1():
    lastupdated = datetime.now()
    rids = request.form.getlist('recallID[]')
    reason = request.form.get('reason')
    psd = request.form.get('psd')
    ped = request.form.get('ped')
    
    if rids and reason:
        sql = "insert into Priority (LastUpdated, PriorityReason, PriorityStartDate, PriorityEndDate, RecallID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, [lastupdated, reason, psd, ped, rids])
        cursor.execute("SELECT * FROM Priority")
        priority = cursor.fetchall()
        dbConn.commit()
        # flash("Recall has been successfully added.")
        return render_template('HighPriority.html', priority=priority)
    else:
        sql = "select * from Recalls"
        cursor.execute(sql)
        recalls= cursor.fetchall()
        # flash('Please select a recall to add.')
        return render_template('AddHighPriorityTable.html', recalls=recalls)
        
    

@app.route('/next-input', methods=['POST'])
def next_input():
    selected_recalls = request.form.get('selectedRecalls')
    recalls = json.loads(selected_recalls) if selected_recalls else []

    return render_template('AddHighPriorityInput.html', recalls=recalls)




@app.route('/search', methods=['GET'])
def search():
    recall_id = request.args.get('recall_id', '').strip()
    cursor = None
    try:
        cursor = dbConn.cursor()
        if not recall_id:
            sql = "SELECT * FROM Recalls"
            cursor.execute(sql)
            recalls = cursor.fetchall()
        else:
            # Query to search for recalls by ID
            sql = "SELECT * FROM Recalls WHERE RecallID = %s"  # Adjust column name as needed
            cursor.execute(sql, (recall_id,))
            recalls = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while searching: " + str(e))
        recalls = []
    finally:
        if cursor:
            cursor.close()  # Ensure the cursor is closed

    if recalls:
        return render_template('Recalls.html', recall=recalls)
    else:
        flash("No recalls found for the given Recall ID.")
        return render_template('Recalls.html', recall=recalls)


@app.route('/searchhighpriority', methods=['GET'])
def searchhigh():
    recall_id = request.args.get('recall_id', '').strip()
    cursor = None
    try:
        cursor = dbConn.cursor()
        if not recall_id:
            sql = "SELECT * FROM Recalls"
            cursor.execute(sql)
            recalls = cursor.fetchall()
        else:
            # Query to search for recalls by ID
            sql = "SELECT * FROM Recalls WHERE RecallID = %s"  # Adjust column name as needed
            cursor.execute(sql, (recall_id,))
            recalls = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while searching: " + str(e))
        recalls = []
    finally:
        if cursor:
            cursor.close()  # Ensure the cursor is closed

    if recalls:
        return render_template('AddHighPriorityTable.html', recall=recalls)
    else:
        flash("No recalls found for the given Recall ID.")
        return render_template('AddHighPriorityTable', recall=recalls)


#Sprint 2


@app.route('/marketlistings')
def marketlistings():
    sql = "select * from MarketListings"
    cursor.execute(sql)
    listings= cursor.fetchall()
    return render_template('MarketListings.html', listings = listings)

@app.route('/addmarketlisting')
def addmarketlisting():
    return render_template('AddMarketListing.html')


@app.route('/addmarketlistings', methods=['POST', 'GET'])
def addmarketlistings():
    marketlistingname = request.form.get('marketlistingname')
    marketlistingdate = request.form.get('marketlistingdate')
    url = request.form.get('url')
    sellername = request.form.get('sellername')
    selleremail = request.form.get('selleremail')
    listingID = request.form.get('listingID')
    units_sold = request.form.get('units_sold')
    product_id = request.form.get('product_id')
    seller_id = request.form.get('seller_id')
    #input validation
    error = False

    if not marketlistingname:
        error = True
        flash('Please provide a Market Listing Name.')
    if not marketlistingdate:
        error = True
        flash('Please provide a Market Listing Date.')
    if not url:
        error = True
        flash('Please provide a URL.')
    if not sellername:
        error = True
        flash('Please provide a Seller Name.')
    if not selleremail:
        error = True
        flash('Please provide a Seller Email.')
    
    if not error:
        
        if not listingID:
            sql = "insert into MarketListings(ListingName, ListingURL, ListingDateTime, UnitsSold, ProductID, SellerID) values(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [marketlistingname, url, marketlistingdate, units_sold, product_id, seller_id])

            listingID = cursor.lastrowid

            sql = "insert into SellerInfo(SellerName, SellerContact) values(%s, %s)"
            cursor.execute(sql, [sellername, selleremail])
            cursor.execute("SELECT * FROM MarketListings")
            listings = cursor.fetchall()
            dbConn.commit()
            flash("New Market Listing has been created.")
        else:
            sql = "update MarketListings set ListingName=%s, ListingURL=%s, ListingDateTime=%s where ListingID=%s "
            cursor.execute(sql, [marketlistingname, url,marketlistingdate, listingID])
            sql = "insert into SellerInfo(SellerName, SellerContact, ListingID) values(%s, %s, %s)"
            cursor.execute(sql, [sellername, selleremail, listingID])
            cursor.execute("SELECT * FROM MarketListings")
            listings = cursor.fetchall()
            dbConn.commit()
            flash("New Market Listing has been successfully updated.")
        return render_template('MarketListings.html', listings=listings )
    else:
        return render_template('AddMarketListing.html', marketlistingname=marketlistingname, marketlistingdate=marketlistingdate, url=url)    
    

@app.route('/violations')
def violations():
    sql = """
        SELECT 
            v.ViolationID, 
            v.ViolationName, 
            v.ViolationFound, 
            v.UserID, 
            ls.Status 
        FROM 
            Violations v
        LEFT JOIN 
            ListingStatus ls ON v.ListingID = ls.ListingID
    """
    cursor.execute(sql)
    violations= cursor.fetchall()
    return render_template('Violations.html', violations=violations)

@app.route('/addviolationsload')
def addviolationsload():
    sql = "select * from SellerInfo"
    cursor.execute(sql)
    seller= cursor.fetchall()

    sql = "select * from Products"
    cursor.execute(sql)
    products= cursor.fetchall()
    return render_template('AddViolation.html', seller=seller, products=products)

@app.route('/addviolations', methods=['GET', 'POST'])
def addviolations():
    if request.method == 'POST':
        marketlistingname = request.form.get('marketlistingname')
        marketlistingdate = request.form.get('marketlistingdate')
        url = request.form.get('url')
        sellername = request.form.get('sellername')
        selleremail = request.form.get('selleremail')
        units = request.form.get('units')
        listingID = request.form.get('listingID')
        pname = request.form.get('listingID')
        #input validation
        error = False

        if not marketlistingname:
            error = True
            flash('Please provide a Market Listing Name.')
        if not marketlistingdate:
            error = True
            flash('Please provide a Market Listing Date.')
        if not url:
            error = True
            flash('Please provide a URL.')
        if not sellername:
            error = True
            flash('Please provide a Seller Name.')
        if not selleremail:
            error = True
            flash('Please provide a Seller Email.')
        
        if not error:
            
            if not listingID:
                #market listing table 
                sql = "insert into MarketListings(ListingName, ListingURL, ListingDateTime, UnitsSold, ProductID) values(%s, %s, %s, %s, %s)"
                cursor.execute(sql, [marketlistingname, url, marketlistingdate, units, pname])

                listingID = cursor.lastrowid
                #seller table
                sql = "insert into SellerInfo(SellerName, SellerContact, ListingID) values(%s, %s, %s)"
                cursor.execute(sql, [sellername, selleremail, listingID])
                #violations table
                sql = "insert into Violations(ViolationName, ViolationFound, ListingID) values(%s, %s, %s, %s)"
                cursor.execute(sql, [marketlistingname,marketlistingdate , listingID])

                cursor.execute("SELECT * FROM MarketListings")
                listings = cursor.fetchall()
                dbConn.commit()
                flash("New Market Listing has been created.")
            else:
                sql = "update MarketListings set ListingName=%s, ListingURL=%s, ListingDateTime=%s where ListingID=%s "
                cursor.execute(sql, [marketlistingname, url,marketlistingdate, listingID])
                sql = "insert into SellerInfo(SellerName, SellerContact, ListingID) values(%s, %s, %s)"
                cursor.execute(sql, [sellername, selleremail, listingID])
                cursor.execute("SELECT * FROM MarketListings")
                listings = cursor.fetchall()
                dbConn.commit()
                flash("New Market Listing has been successfully updated.")
            return render_template('MarketListings.html', listings=listings )
        else:
            sql = "select * from SellerInfo"
            cursor.execute(sql)
            seller= cursor.fetchall()

            sql = "select * from Products"
            cursor.execute(sql)
            products= cursor.fetchall()
            return render_template('AddMarketListing.html', marketlistingname=marketlistingname, marketlistingdate=marketlistingdate, url=url, seller = seller, units=units, products=products)  
    else:
        sql = "select * from SellerInfo"
        cursor.execute(sql)
        seller= cursor.fetchall()

        sql = "select * from Products"
        cursor.execute(sql)
        products= cursor.fetchall()
        return render_template('AddMarketListing.html', marketlistingname=marketlistingname, marketlistingdate=marketlistingdate, url=url, seller = seller, units=units, products=products)
   
    

@app.route('/reports2')
def reports2():
    return render_template('ViolationReports.html')
@app.route('/updatestatus', methods=['GET', 'POST'])
def updatestatus():
    if request.method == 'POST':
        # Get the selected listings from the form
        selected_listings = request.form.getlist('listings[]')
        
        if not selected_listings:
            flash('Please select at least one listing.')
            return redirect(url_for('marketlistings'))
        
        # Store selected listings in session
        session['selected_listings'] = selected_listings
        
        # Fetch the existing statuses from the ListingStatus table for the dropdown
        sql = "SELECT DISTINCT Status FROM ListingStatus"
        try:
            cursor.execute(sql)
            statuses = cursor.fetchall()
        except Exception as e:
            flash(f"Error fetching statuses: {str(e)}")
            return redirect(url_for('marketlistings'))
        
        return render_template('UpdateStatus.html', statuses=statuses)
    
    return redirect(url_for('marketlistings'))


@app.route('/update_status', methods=['POST'])
def process_update_status():
    status = request.form.get('status')
    selected_listings = session.get('selected_listings', [])
    
    if selected_listings and status:
        try:
            for listing_id in selected_listings:
                # Check if a status record exists for this listing in ListingStatus
                check_sql = "SELECT * FROM ListingStatus WHERE ListingID = %s"
                cursor.execute(check_sql, [listing_id])
                existing_status = cursor.fetchone()
                
                if existing_status:
                    # Update existing status
                    update_sql = "UPDATE ListingStatus SET Status = %s WHERE ListingID = %s"
                    cursor.execute(update_sql, [status, listing_id])
                else:
                    # Insert new status record
                    insert_sql = "INSERT INTO ListingStatus (Status, ListingID) VALUES (%s, %s)"
                    cursor.execute(insert_sql, [status, listing_id])
            
            dbConn.commit()
            flash('Status updated successfully!')
        except Exception as e:
            dbConn.rollback()
            flash(f'Error updating status: {str(e)}')
    else:
        flash('No listings selected or status not specified')
    
    # Clear the session
    session.pop('selected_listings', None)
    return redirect(url_for('marketlistings'))

#Sprint 3


@app.route('/outcomes')
def outcomes():
    
    # sql = "SELECT u.Username FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
    # sql = "select * from Outcome"
    sql = "SELECT o.OutcomeID, u.Username, o.Decision, o.Rationale, o.ResponseID, o.UserID FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
    cursor.execute(sql)
    outcomes = cursor.fetchall()
    return render_template('OutcomesTable.html', outcomes=outcomes)


@app.route('/logoutcomes')
def logoutcomes():
    # sql = "select * from Outcome"
    sql="SELECT o.OutcomeID, u.Username, o.Decision, o.Rationale, o.ResponseID, o.UserID FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
    cursor.execute(sql)
    outcomes= cursor.fetchall()
    return render_template('LogOutcome.html', outcomes=outcomes)

@app.route('/logoutcome', methods=['GET', 'POST'])
def logoutcome():
    if request.method == 'POST':
        responseid = request.form.getlist('responseid[]')
        responseid_selected = responseid[0] if responseid else None
        outcomeid = request.form.get('outcomeid')
        decision = request.form.get('decision')
        name = request.form.get('name')

        error = False

        # Validate inputs
        if not responseid_selected:
            error = True
            flash("Please provide a ResponseID!")

        if not outcomeid:
            error = True
            flash("Please provide an OutcomeID!")

        if not decision:
            error = True
            flash("Please provide a Decision!")

        if not name:
            error = True
            flash("Please provide an Investigator Name!")

        # Check database constraints
        if not error:
            user_check_sql = "SELECT UserID FROM Users WHERE Username = %s"
            cursor.execute(user_check_sql, [name])
            user = cursor.fetchone()
            if not user:
                error = True
                flash(f"User with username '{name}' does not exist!")

            outcome_check_sql = "SELECT * FROM Outcome WHERE OutcomeID = %s"
            cursor.execute(outcome_check_sql, [outcomeid])
            outcome = cursor.fetchone()
            if not outcome:
                error = True
                flash(f"OutcomeID '{outcomeid}' does not exist!")

            response_check_sql = "SELECT * FROM Response WHERE ResponseID = %s"
            cursor.execute(response_check_sql, [responseid_selected])
            response = cursor.fetchone()
            if not response:
                error = True
                flash(f"ResponseID '{responseid_selected}' does not exist!")

        if not error:
            sql = """
            UPDATE Outcome 
            SET ResponseID = %s, Decision = %s, UserID = (SELECT UserID FROM Users WHERE Username = %s)
            WHERE OutcomeID = %s
            """
            cursor.execute(sql, [responseid_selected, decision, name, outcomeid])
            dbConn.commit()
            flash("Outcome has been logged!")
            return redirect('/violationresponses')

        # Reload form with errors
        sql = "SELECT o.OutcomeID, u.Username, o.Decision, o.Rationale, o.ResponseID, o.UserID FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
        cursor.execute(sql)
        outcomes = cursor.fetchall()
        return render_template('LogOutcome.html', outcomes=outcomes, responseid=responseid_selected, outcomeid=outcomeid, decision=decision, name=name)
    else:
        # Load outcomes for GET request
        sql = "SELECT o.OutcomeID, u.Username, o.Decision, o.Rationale, o.ResponseID, o.UserID FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
        cursor.execute(sql)
        outcomes = cursor.fetchall()
        return render_template('LogOutcome.html', outcomes=outcomes, responseid=None, outcomeid=None, decision=None, name=None)


@app.route('/violationresponses')
def violationresponses():
    sql = "select * from Response"
    cursor.execute(sql)
    response= cursor.fetchall()
    return render_template('ViolationResponses.html', response=response)

@app.route('/next-logoutcome', methods=['POST'])
def next_logoutcome():
    selected_responses = request.form.get('selectedResponses')
    responses = json.loads(selected_responses) if selected_responses else []

    # sql = "select * from Outcome"
    sql = "SELECT o.OutcomeID, u.Username, o.Decision, o.Rationale, o.ResponseID FROM Users u JOIN Outcome o ON u.UserId = o.UserId;"
    cursor.execute(sql)
    outcomes= cursor.fetchall()
    return render_template('LogOutcome.html', responses=responses, outcomes=outcomes)





        
    
@app.route('/letterssent')
def letters_sent():
    # SQL query to fetch data from the LettersSent table
    sql = """
        SELECT 
            `LettersSent`.`LetterID`,
            `LettersSent`.`LetterText`,
            `LettersSent`.`LetterDateTime`,
            `LettersSent`.`ViolationID`,
            `LettersSent`.`SellerID`
        FROM `CPSCProject`.`LettersSent`;
    """
    
    # Execute the query
    cursor.execute(sql)
    letters = cursor.fetchall()

    # Pass the fetched data to the template
    return render_template('LettersSent.html', letters=letters)