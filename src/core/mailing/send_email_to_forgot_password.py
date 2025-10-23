from textwrap import dedent
from core.database.models import User
from .base_send_email import send_email
from core.jinja.jinja_templates import templates


async def send_pasword_reset_email(
    user: User,
    reset_link: str,
):
    recipient = user.email
    subject = "Forgot password for site.com"
    
    plain_content = dedent(
        f"""\
        Dear {recipient},
        
        Please follow the link to reset your old password:
        {reset_link}
        
        Your site admin,
        ©️ 2025.
        """
    )
    
    template = templates.get_template(
        "mailing/password/forgot_password.html"
    )
    
    context = {
        "user": user,
        "reset_link": reset_link,
    }
    
    html_content = template.render(context)
    
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )