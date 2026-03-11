"""Project management CLI."""
# ruff: noqa: E402 - Import at bottom to avoid circular imports

import asyncio

import click
from tabulate import tabulate


@click.group()
@click.version_option(version="0.1.0", prog_name="med_agent")
def cli():
    """med_agent management CLI."""


# === Server Commands ===
@cli.group("server")
def server_cli():
    """Server commands."""


@server_cli.command("run")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, type=int, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def server_run(host: str, port: int, reload: bool):
    """Run the development server."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@server_cli.command("routes")
def server_routes():
    """Show all registered routes."""
    from app.main import app

    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            for method in route.methods - {"HEAD", "OPTIONS"}:
                routes.append([method, route.path, getattr(route, "name", "-")])

    click.echo(tabulate(routes, headers=["Method", "Path", "Name"]))


# === User Commands ===
@cli.group("user")
def user_cli():
    """User management commands."""


@user_cli.command("create")
@click.option("--email", prompt=True, help="User email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="User password")
@click.option("--role", type=click.Choice(["user", "admin"]), default="user", help="User role")
@click.option("--superuser", is_flag=True, default=False, help="Create as superuser")
def user_create(email: str, password: str, role: str, superuser: bool):
    """Create a new user."""
    from app.core.exceptions import AlreadyExistsError
    from app.db.models.user import UserRole
    from app.schemas.user import UserCreate, UserUpdate
    from app.services.user import UserService

    async def _create():
        service = UserService()
        try:
            user = await service.register(
                UserCreate(
                    email=email,
                    password=password,
                    role=UserRole.ADMIN if role == "admin" else UserRole.USER,
                )
            )
            if superuser:
                user = await service.update(
                    str(user.id),
                    UserUpdate(
                        role=UserRole.ADMIN,
                        is_active=True,
                    ),
                )
                user.is_superuser = True
                await user.save()
            return user
        except AlreadyExistsError as exc:
            click.secho(f"User already exists: {exc.details.get('email', email)}", fg="red")
            return None

    user = asyncio.run(_create())
    if user:
        click.secho(f"User created: {user.email} (role: {user.role})", fg="green")


@user_cli.command("create-admin")
@click.option("--email", prompt=True, help="Admin email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
def user_create_admin(email: str, password: str):
    """Create an admin user."""
    from app.core.exceptions import AlreadyExistsError
    from app.db.models.user import UserRole
    from app.schemas.user import UserCreate, UserUpdate
    from app.services.user import UserService

    async def _create():
        service = UserService()
        try:
            user = await service.register(
                UserCreate(
                    email=email,
                    password=password,
                    role=UserRole.ADMIN,
                )
            )
            user = await service.update(
                str(user.id),
                UserUpdate(role=UserRole.ADMIN, is_active=True),
            )
            user.is_superuser = True
            await user.save()
            return user
        except AlreadyExistsError as exc:
            click.secho(f"User already exists: {exc.details.get('email', email)}", fg="red")
            return None

    user = asyncio.run(_create())
    if user:
        click.secho(f"Admin user created: {user.email}", fg="green")
        click.echo("This user has admin role and superuser privileges.")


@user_cli.command("set-role")
@click.argument("email")
@click.option("--role", type=click.Choice(["user", "admin"]), required=True, help="New role")
def user_set_role(email: str, role: str):
    """Change a user's role."""
    from app.core.exceptions import NotFoundError
    from app.db.models.user import UserRole
    from app.schemas.user import UserUpdate
    from app.services.user import UserService

    async def _set_role():
        service = UserService()
        user = await service.get_by_email(email)
        if user is None:
            raise NotFoundError(message="User not found", details={"email": email})
        return await service.update(
            str(user.id),
            UserUpdate(role=UserRole.ADMIN if role == "admin" else UserRole.USER),
        )

    try:
        user = asyncio.run(_set_role())
        click.secho(f"User {user.email} role updated to: {role}", fg="green")
    except NotFoundError:
        click.secho(f"User not found: {email}", fg="red")


@user_cli.command("list")
def user_list():
    """List all users."""
    from app.services.user import UserService

    async def _list():
        service = UserService()
        return await service.get_multi(limit=1000)

    users = asyncio.run(_list())
    if not users:
        click.echo("No users found.")
        return

    table = [[u.id, u.email, u.role, u.is_active, u.is_superuser] for u in users]
    click.echo(tabulate(table, headers=["ID", "Email", "Role", "Active", "Superuser"]))


# === Custom Commands ===
@cli.group("cmd")
def cmd_cli():
    """Custom commands."""


# Register all custom commands from app/commands/
from app.commands import register_commands

register_commands(cmd_cli)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
