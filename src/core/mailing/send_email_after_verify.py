from textwrap import dedent
from core.database.models import User
from .base_send_email import send_email
from core.jinja.jinja_templates import templates

async def send_answer_after_verify(
    user: User,
):
    recipient = user.email
    subject = "Email confirmed"
    
    plain_content = dedent(
        f"""\
        Dear {recipient},
        
        Email was successfully confirmed!
        
        Your site admin,
        ©️ 2025.
        """
    )
    
    
    template = templates.get_template(
        "mailing/email-verifying/after_verify.html"
    )
    
    context = {
        "user": user,
    }
    
    html_content = template.render(context)
    
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content
    )
    