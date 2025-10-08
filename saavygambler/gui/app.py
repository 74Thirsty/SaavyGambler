"""KivyMD powered application for the SaavyGambler toolkit."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Optional

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

from .controller import (
    StatTrackerController,
    SummaryRow,
    format_event_summary,
    format_player_summary,
    format_team_summary,
)


class _BaseTab(MDBoxLayout, MDTabsBase):
    """Common functionality shared by all tabs."""

    def __init__(self, *, app: "StatTrackerApp", title: str, **kwargs) -> None:
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(16), **kwargs)
        self.app = app
        self.text = title
        self._status_label = MDLabel(
            text="",
            theme_text_color="Secondary",
            halign="left",
            size_hint_y=None,
            height=dp(20),
        )
        self._results = MDList(size_hint_y=None)
        self._results.bind(minimum_height=self._results.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self._results)
        self.add_widget(self._status_label)
        self.add_widget(scroll)

    def set_status(self, message: str) -> None:
        self._status_label.text = message

    def clear_results(self) -> None:
        self._results.clear_widgets()

    def populate_results(self, rows: Iterable[SummaryRow]) -> None:
        self.clear_results()
        count = 0
        for row in rows:
            if row.subtitle:
                item = TwoLineListItem(text=row.title, secondary_text=row.subtitle)
            else:
                item = OneLineListItem(text=row.title)
            self._results.add_widget(item)
            count += 1
        if count == 0:
            self.set_status("No results yet. Try a different search.")
        else:
            self.set_status(f"Showing {count} result{'s' if count != 1 else ''}.")

    def on_error(self, error: Exception) -> None:
        self.set_status(str(error))


class _TeamSearchTab(_BaseTab):
    def __init__(self, *, app: "StatTrackerApp") -> None:
        super().__init__(app=app, title="Teams")
        self._input = MDTextField(
            hint_text="Search for a team",
            helper_text="Enter part of the team name (e.g., Warriors)",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(48),
        )
        self._button = MDRaisedButton(text="Search", on_release=self._on_search)
        controls = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(48))
        controls.add_widget(self._input)
        controls.add_widget(self._button)
        self.add_widget(controls, index=1)

    def _on_search(self, *_args) -> None:
        query = (self._input.text or "").strip()
        if not query:
            self.set_status("Enter a team name to start searching.")
            return
        self.set_status("Searching for teams…")
        self.app.run_task(
            task=lambda: self.app.controller.search_teams(query),
            on_success=self._handle_results,
            on_error=self.on_error,
        )

    def _handle_results(self, teams) -> None:
        rows = [format_team_summary(team) for team in teams]
        self.populate_results(rows)


class _EventLookupTab(_BaseTab):
    def __init__(self, *, app: "StatTrackerApp") -> None:
        super().__init__(app=app, title="Events")
        self._input = MDTextField(
            hint_text="Lookup events",
            helper_text="Comma-separated event IDs",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(48),
        )
        self._button = MDRaisedButton(text="Lookup", on_release=self._on_lookup)
        controls = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(48))
        controls.add_widget(self._input)
        controls.add_widget(self._button)
        self.add_widget(controls, index=1)

    def _parse_ids(self) -> Iterable[str]:
        value = (self._input.text or "").strip()
        for raw in value.split(","):
            normalized = raw.strip()
            if normalized:
                yield normalized

    def _on_lookup(self, *_args) -> None:
        event_ids = list(self._parse_ids())
        if not event_ids:
            self.set_status("Add one or more event IDs to fetch details.")
            return
        self.set_status("Loading events…")
        self.app.run_task(
            task=lambda: self.app.controller.lookup_events(event_ids),
            on_success=self._handle_results,
            on_error=self.on_error,
        )

    def _handle_results(self, events) -> None:
        rows = [format_event_summary(event) for event in events]
        self.populate_results(rows)


class _PlayerStatsTab(_BaseTab):
    def __init__(self, *, app: "StatTrackerApp") -> None:
        super().__init__(app=app, title="Players")
        self._input = MDTextField(
            hint_text="Player stats",
            helper_text="Comma-separated player IDs",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=dp(48),
        )
        self._button = MDRaisedButton(text="Fetch", on_release=self._on_fetch)
        controls = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(48))
        controls.add_widget(self._input)
        controls.add_widget(self._button)
        self.add_widget(controls, index=1)

    def _parse_ids(self) -> Iterable[str]:
        value = (self._input.text or "").strip()
        for raw in value.split(","):
            normalized = raw.strip()
            if normalized:
                yield normalized

    def _on_fetch(self, *_args) -> None:
        player_ids = list(self._parse_ids())
        if not player_ids:
            self.set_status("Provide one or more player IDs to fetch stats.")
            return
        self.set_status("Fetching player statistics…")
        self.app.run_task(
            task=lambda: self.app.controller.get_player_stats(player_ids),
            on_success=self._handle_results,
            on_error=self.on_error,
        )

    def _handle_results(self, players) -> None:
        rows = [format_player_summary(player) for player in players]
        self.populate_results(rows)


class StatTrackerApp(MDApp):
    """KivyMD application exposing SaavyGambler features."""

    def __init__(self, controller: Optional[StatTrackerController] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.controller = controller or StatTrackerController()
        self._executor = ThreadPoolExecutor(max_workers=4)

    def build(self) -> MDScreen:
        self.title = "SaavyGambler"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"
        screen = MDScreen()
        root = MDBoxLayout(orientation="vertical")
        root.add_widget(MDTopAppBar(title="SaavyGambler", elevation=4))
        tabs = MDTabs()
        self._team_tab = _TeamSearchTab(app=self)
        self._event_tab = _EventLookupTab(app=self)
        self._player_tab = _PlayerStatsTab(app=self)
        tabs.add_widget(self._team_tab)
        tabs.add_widget(self._event_tab)
        tabs.add_widget(self._player_tab)
        root.add_widget(tabs)
        screen.add_widget(root)
        return screen

    def run_task(
        self,
        *,
        task: Callable[[], object],
        on_success: Callable[[object], None],
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        """Execute a blocking task on a worker thread and update the UI."""

        def _handle_success(result: object) -> None:
            if on_success:
                on_success(result)

        def _handle_error(exc: Exception) -> None:
            if on_error:
                on_error(exc)
            else:
                self._team_tab.set_status(str(exc))

        def _worker() -> None:
            try:
                result = task()
            except Exception as exc:  # pragma: no cover - UI feedback
                Clock.schedule_once(lambda _dt: _handle_error(exc))
            else:
                Clock.schedule_once(lambda _dt: _handle_success(result))

        self._executor.submit(_worker)

    def on_stop(self) -> None:
        super().on_stop()
        self._executor.shutdown(wait=False, cancel_futures=True)


def main() -> None:
    """Entry point used by console scripts and ``python -m`` invocations."""

    StatTrackerApp().run()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
