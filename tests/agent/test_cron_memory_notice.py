"""Tests for the cron memory-disabled notice (issue #38647).

Cron runs force ``skip_memory=True``, which silently blocks all MEMORY.md /
USER.md persistence while the job still exits 0. ``_cron_memory_disabled_notice``
decides when that silent loss is surprising enough to surface to the user.
"""

from agent.agent_init import _cron_memory_disabled_notice


class TestCronMemoryDisabledNotice:
    def test_notice_when_memory_enabled(self):
        notice = _cron_memory_disabled_notice(True, "cron", {"memory_enabled": True})
        assert notice and "#38647" in notice

    def test_notice_when_user_profile_enabled(self):
        notice = _cron_memory_disabled_notice(True, "cron", {"user_profile_enabled": True})
        assert notice is not None

    def test_notice_when_external_provider_configured(self):
        notice = _cron_memory_disabled_notice(True, "cron", {"provider": "honcho"})
        assert notice is not None

    def test_no_notice_when_memory_not_configured(self):
        assert _cron_memory_disabled_notice(True, "cron", {}) is None
        assert _cron_memory_disabled_notice(True, "cron", None) is None

    def test_no_notice_for_blank_provider(self):
        assert _cron_memory_disabled_notice(True, "cron", {"provider": "   "}) is None

    def test_no_notice_for_non_cron_platforms(self):
        # Other skip_memory callers (subagents, batch, curator) don't set
        # platform="cron" and shouldn't be warned about.
        assert _cron_memory_disabled_notice(True, "cli", {"memory_enabled": True}) is None
        assert _cron_memory_disabled_notice(True, None, {"memory_enabled": True}) is None
        assert _cron_memory_disabled_notice(True, "telegram", {"memory_enabled": True}) is None

    def test_no_notice_when_memory_not_skipped(self):
        assert _cron_memory_disabled_notice(False, "cron", {"memory_enabled": True}) is None
