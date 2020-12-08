from datetime import datetime as dt, timedelta as td
from app.models import db, BlockedIPs
from flask import  redirect, flash, url_for

def banIP(ip,error):
    ip_info = BlockedIPs.query.filter_by(ip=ip).first()
    if(ip_info == None):
        time = dt.now()
        ip_info = BlockedIPs(
            ip = ip, 
            last_timestamp = time,
            timeout = time + td(minutes = 15)
        )
        db.session.add(ip_info)
    else:
        time = dt.now()
        prev_time_diference = ip_info.timeout - ip_info.last_timestamp
        ip_info.last_timestamp = time
        ip_info.timeout = min(time + td(seconds = prev_time_diference.seconds * 2), time + td(hours = 24))
    db.session.commit()
    flash(f"{error} Try again in {str(ip_info.timeout - ip_info.last_timestamp).split('.', 2)[0]}", "error")
    