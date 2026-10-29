from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

console = Console()

# 1. Простая панель
console.print(Panel("Простая панель с текстом"))

# 2. Заголовок и подзаголовок
console.print(
    Panel(
        "Текст внутри панели",
        title="[bold cyan]Заголовок[/]",
        title_align="left",            # left | center | right
        subtitle="[dim]Подзаголовок[/]",
        subtitle_align="right",
    )
)

# 3. Стили рамок
for name, b in [("ROUNDED", box.ROUNDED), ("SQUARE", box.SQUARE),
                ("DOUBLE", box.DOUBLE), ("HEAVY", box.HEAVY),
                ("ASCII", box.ASCII), ("MINIMAL", box.MINIMAL)]:
    console.print(Panel(f"box.{name}", box=b, width=30, border_style="yellow"))

# 4. Цвета: рамка, фон и текст
console.print(
    Panel(
        "[bold]Белый текст на синем фоне[/bold]",
        border_style="bold green",
        style="white on dark_blue",
    )
)

# 5. Отступы (padding): (вертикаль, горизонталь) или (сверху, справа, снизу, слева)
console.print(Panel("С большими отступами", padding=(2, 8)))

# 6. Panel.fit: ширина по содержимому
console.print(Panel.fit("Компактная панель", border_style="magenta"))

# 7. Фиксированные размеры
console.print(Panel("Ширина 40, высота 5", width=40, height=5))

# 8. Текст по центру внутри панели
console.print(Panel(Text("Центрированный текст", justify="center"), expand=True))

# 9. Таблица внутри панели
table = Table(box=box.SIMPLE, header_style="bold magenta")
table.add_column("Имя")
table.add_column("Статус", justify="center")
table.add_row("Анна", "[green]OK[/green]")
table.add_row("Борис", "[red]FAIL[/red]")
console.print(Panel(table, title="Таблица в панели", border_style="blue"))

# 10. Код внутри панели
code = '''def hello(name):
    return f"Hello, {name}!"'''
console.print(
    Panel(
        Syntax(code, "python", theme="monokai", line_numbers=True),
        title="Код",
        border_style="green",
    )
)

# 11. Несколько элементов через Group
console.print(
    Panel(
        Group(
            Text("Первая строка", style="bold"),
            Panel("Вложенная панель", border_style="red"),
            Text("Последняя строка", style="italic dim"),
        ),
        title="Группа элементов",
    )
)

# 12. Разные варианты содержимого в одном дашборде
console.print(
    Panel(
        "[bold green]Система работает нормально[/bold green]\n"
        "CPU: [cyan]23%[/cyan]\n"
        "RAM: [yellow]61%[/yellow]\n"
        "Диск: [red]92%[/red]",
        title="[bold]Мониторинг[/bold]",
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 3),
    )
)