from textwrap import dedent
from core.database.models import User
from .base_send_email import send_email
from core.jinja.jinja_templates import templates

async def send_verification_email(
    user: User,
    verification_link: str,
):
    recipient = user.email
    subject = "Confirm your email for site.com"
    
    plain_content = dedent(
        f"""\
        Dear {recipient},
        Please follow the libk to verify your email:
        {verification_link}
        
        Your site admin,
        ©️ 2025.
        """
    )
    
    # html format:
    
    template = templates.get_template(
        "mailing/email-verifying/before_verify.html"
    )
    
    context = {
        "user": user,
        "verification_link": verification_link,
    }
    
    html_content = template.render(context)
    
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content
    )
    