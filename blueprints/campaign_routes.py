#
# from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request
#
# from schemas import db
# from schemas.campaign_models import Campaign
# from schemas.user_models import User
#
# campaigns_bp = Blueprint('campaigns', __name__, template_folder='templates/campaigns')
#
#
# @campaigns_bp.route('/create_campaign', methods=['GET', 'POST'])
# def create_campaign():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         name = request.form.get('name')
#
#         if not user_id or not name:
#             flash('User ID and Name are required.', 'danger')
#             return redirect(url_for('campaigns.create_campaign'))
#
#         user = User.query.get(user_id)
#         if not user:
#             flash('User not found.', 'danger')
#             return redirect(url_for('campaigns.create_campaign'))
#
#         campaign = Campaign(name=name, owner=user)
#         db.session.add(campaign)
#         db.session.commit()
#         flash('Campaign created!', 'success')
#         return redirect(url_for('campaigns.create_campaign'))
#
#     return render_template('create_campaign.html')