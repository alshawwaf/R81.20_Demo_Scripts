#!/usr/bin/env python3
"""
This script will create the following objects for the Workflow demo:

Permission Profiles
 - policy_approver: admins have permission to approve policy changes.
 - policy_auto_approve: admins with this profile can change their own changes only.
 - policy_no_auto_approve: Changes are submitted for approval.
 
Administrators:
 - t1_admin: Tier 1 admin with policy_no_auto_approve profile.
 - t2_admin: Tier 2 admin with policy_auto_approve profile.
 - t3_admin: Tier 3 Admin with policy_approver profile.

SmartTasks
 - Send Mail After Submit: send an Email when changes are submitted.
 
Mail-Server 
 - Mail_<ip_of_mail_server>: Mail server to handle Emails from SmartTasks.
 
"""
import argparse
import logging
import sys

from cpapi import APIClient, APIClientArgs

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    """

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", default="admin")
    parser.add_argument("-p", "--password", default="Cpwins!1")
    parser.add_argument("-m", "--management", default="203.0.113.120")
    parser.add_argument("-d", "--domain", default="System Data")
    parser.add_argument("-s", "--server", default="203.0.113.200")  

    parsed_args = parser.parse_args()

    client_args = APIClientArgs(server=parsed_args.management)
    with APIClient(client_args) as client:
        # login to the "System Data" domian to create admins and permission profiles
        login = client.login(username=parsed_args.username,
                             password=parsed_args.password, domain=parsed_args.domain)
        if login.success:
            log.info(f"login succeeded to {parsed_args.domain}")
        else:
            log.error(login.error_message)
            sys.exit(1)
        # create permission profiles
        add_approver_res = client.api_call(
            "add-domain-permissions-profile", payload={"name": "policy_approver", "management": {"approve-or-reject-sessions": "true"}, "comments": "Approve Policy changes"})

        if add_approver_res.success:
            log.info("Added policy_approver Profile")
        else:
            log.error(add_approver_res.error_message)

        add_auto_approve = client.api_call(
            "add-domain-permissions-profile", payload={"name": "policy_auto_approve", "comments": "Approve current local changes only"})

        if add_auto_approve.success:
            log.info("Added add_auto_approve Profile")
        else:
            log.error(add_auto_approve.error_message)

        add_no_auto_approve = client.api_call(
            "add-domain-permissions-profile", payload={"name": "policy_no_auto_approve", "management": {"publish-sessions": "false"}, "comments": "Policy is submitted for approval"})

        if add_no_auto_approve.success:
            log.info("Added add_no_auto_approve Profile")
        else:
            log.error(add_no_auto_approve.error_message)
            
        # publish after creating permission profiles.
        publish_profiles_res = client.api_call(
            "publish", payload={})

        if publish_profiles_res.success:
            log.info("Publishing session after permission profiles creation")
        else:
            log.error(publish_profiles_res.error_message)

        # create administrators
        add_t3_admin_res = client.api_call(
            "add-administrator", payload={"name": "t3_admin", "password": "Cpwins!1", "must-change-password": "false", "authentication-method": "check point password", "permissions-profile": "policy_approver"})

        if add_t3_admin_res.success:
            log.info("Added t3_admin administrator")
        else:
            log.error(add_t3_admin_res.error_message)

        add_t2_admin_res = client.api_call(
            "add-administrator", payload={"name": "t2_admin", "password": "Cpwins!1", "must-change-password": "false", "authentication-method": "check point password", "permissions-profile": "policy_auto_approve"})

        if add_t2_admin_res.success:
            log.info("Added t2_admin administrator")
        else:
            log.error(add_t2_admin_res.error_message)

        add_t1_admin_res = client.api_call(
            "add-administrator", payload={"name": "t1_admin", "password": "Cpwins!1", "must-change-password": "false", "authentication-method": "check point password", "permissions-profile": "policy_no_auto_approve"})

        if add_t1_admin_res.success:
            log.info("Added t1_admin administrator")
        else:
            log.error(add_t1_admin_res.error_message)

        # publish after creating administrators
        publish_admins_res = client.api_call(
            "publish", payload={})

        if publish_admins_res.success:
            log.info("Publishing session after administrators creation")
        else:
            log.error(publish_admins_res.error_message)
            
    with APIClient(client_args) as client:
        # login to local domain to create SmartTask and Mail Server
        login = client.login(username=parsed_args.username,
                             password=parsed_args.password)
        if login.success:
            log.info("login succeeded to local domain")
        else:
            log.error(login.error_message)
             
        if parsed_args.server:
            add_email_server = client.api_call(
            "add-smtp-server", payload={"name": f"mail_{parsed_args.server}", "server": f"{parsed_args.server}","port" : "25","encryption" : "none", "comments":"added by workflow demo script"})
            if add_email_server.success:
                log.info(f"Created Email server {parsed_args.server}")
            else:
                log.error(add_email_server.error_message)
            
            publish_profiles_res = client.api_call(
            "publish", payload={})

            if publish_profiles_res.success:
                log.info(f"Publishing session after adding the Email server {parsed_args.server}")
            else:
                log.error(publish_profiles_res.error_message)
                
                           
        add_smart_task_res = client.api_call(
            "add-smart-task", payload={"name": "Send Mail After Submit", "trigger": "After Submit", "description": "Notifying via email about a submitted session with change report attached.", "action": {"send-mail": {"mail-settings": {"subject": "A session was submitted", "recipients": "t3_admin@alshawwaf.ca", "sender-email": "policy@alshawwaf.ca", "body": "Please review my session", "attachment": "changes_report"}, "smtp-server": f"mail_{parsed_args.server}"}}, "enabled": "true"})

        if add_smart_task_res.success:
            log.info("Publishing session after administrators creation")
        else:
            log.error(add_smart_task_res.error_message)

        # publish after creating SmartTasks and Mail server
        publish_smart_task_res = client.api_call(
            "publish", payload={})

        if publish_smart_task_res.success:
            log.info("Publishing session after SmartTask creation")
        else:
            log.error(publish_smart_task_res.error_message)

            
if __name__ == "__main__":
    main()