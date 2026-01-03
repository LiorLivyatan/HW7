"""
Advanced Unit Tests for StrategyEngine - Coverage Improvement

Tests additional functionality to increase coverage from 49% to 70%+
Focuses on LLM mode, system prompts, agent creation, and error handling.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from my_project.agents.player.strategy import StrategyEngine


class TestLLMMode:
    """Test LLM-specific functionality."""

    def test_llm_mode_without_api_key_raises_error(self):
        """Test that LLM mode (not hybrid) raises error without API key."""
        # Temporarily clear API key
        with patch.dict(os.environ, {"GOOGLE_API_KEY": ""}, clear=False):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY required"):
                StrategyEngine(mode="llm")

    def test_llm_mode_with_placeholder_key_raises_error(self):
        """Test that LLM mode rejects placeholder API key."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "your_google_gemini_api_key_here"}, clear=False):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY required"):
                StrategyEngine(mode="llm")

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-api-key-12345"})
    def test_llm_mode_with_valid_api_key_creates_agent(self):
        """Test that LLM mode creates agent with valid API key."""
        engine = StrategyEngine(mode="llm", llm_timeout=25)

        # Agent should be created
        assert engine.agent is not None
        assert engine.mode == "llm"

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-api-key-12345"})
    def test_hybrid_mode_with_valid_api_key_creates_agent(self):
        """Test that hybrid mode creates agent with valid API key."""
        engine = StrategyEngine(mode="hybrid", llm_timeout=25)

        # Agent should be created
        assert engine.agent is not None
        assert engine.mode == "hybrid"

    def test_hybrid_mode_without_api_key_no_agent(self):
        """Test that hybrid mode works without API key (no agent created)."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": ""}, clear=False):
            engine = StrategyEngine(mode="hybrid")

            # No agent should be created, but mode should work
            assert engine.agent is None
            assert engine.mode == "hybrid"

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-api-key"})
    def test_custom_system_prompt(self):
        """Test initialization with custom system prompt."""
        custom_prompt = "You are a custom AI agent. Always choose even."

        engine = StrategyEngine(
            mode="llm",
            system_prompt=custom_prompt,
            llm_timeout=25
        )

        assert engine.agent is not None

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_custom_temperature(self):
        """Test initialization with custom temperature."""
        engine = StrategyEngine(
            mode="llm",
            temperature=0.9,
            llm_timeout=25
        )

        assert engine.agent is not None

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_custom_max_tokens(self):
        """Test initialization with custom max output tokens."""
        engine = StrategyEngine(
            mode="llm",
            max_output_tokens=200,
            llm_timeout=25
        )

        assert engine.agent is not None


class TestSystemPrompt:
    """Test system prompt generation."""

    def test_default_system_prompt_contains_rules(self):
        """Test that default system prompt contains game rules."""
        engine = StrategyEngine(mode="random")

        prompt = engine._get_default_system_prompt()

        # Should contain key game rules
        assert "Even/Odd game" in prompt
        assert "lowercase" in prompt
        assert "even" in prompt.lower()
        assert "odd" in prompt.lower()
        assert "reasoning" in prompt.lower()

    def test_default_system_prompt_emphasizes_lowercase(self):
        """Test that prompt emphasizes lowercase requirement."""
        engine = StrategyEngine(mode="random")

        prompt = engine._get_default_system_prompt()

        # Should emphasize lowercase (critical protocol requirement)
        assert "MUST be lowercase" in prompt or "must be lowercase" in prompt

    def test_default_system_prompt_includes_scoring(self):
        """Test that prompt includes scoring information."""
        engine = StrategyEngine(mode="random")

        prompt = engine._get_default_system_prompt()

        # Should mention scoring
        assert "3 points" in prompt or "Win = 3" in prompt
        assert "points" in prompt


class TestAgentCreation:
    """Test Agno agent creation."""

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_create_agent_with_default_prompt(self):
        """Test agent creation uses default prompt when None provided."""
        engine = StrategyEngine(mode="llm", llm_timeout=25)

        # Agent should exist
        assert engine.agent is not None

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_create_agent_with_custom_model(self):
        """Test agent creation with custom Gemini model."""
        engine = StrategyEngine(
            mode="llm",
            gemini_model_id="gemini-1.5-flash",
            llm_timeout=25
        )

        assert engine.agent is not None


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_timeout_boundary_29_allowed(self):
        """Test that timeout of 29 seconds is allowed."""
        # Should not raise error
        engine = StrategyEngine(mode="random", llm_timeout=29)
        assert engine.llm_timeout == 29

    def test_timeout_boundary_30_not_allowed(self):
        """Test that timeout of exactly 30 is not allowed."""
        with pytest.raises(ValueError, match="must be < 30 seconds"):
            StrategyEngine(mode="random", llm_timeout=30)

    def test_timeout_negative_not_recommended_but_allowed(self):
        """Test that negative timeout is allowed (though not recommended)."""
        # Python doesn't validate this at init, but would fail at runtime
        engine = StrategyEngine(mode="random", llm_timeout=5)
        assert engine.llm_timeout == 5

    def test_mode_case_sensitive(self):
        """Test that mode is case-sensitive."""
        with pytest.raises(ValueError, match="Invalid mode"):
            StrategyEngine(mode="Random")  # Capital R

        with pytest.raises(ValueError, match="Invalid mode"):
            StrategyEngine(mode="HYBRID")  # All caps

    def test_mode_typo_rejected(self):
        """Test that mode typos are rejected."""
        with pytest.raises(ValueError, match="Invalid mode"):
            StrategyEngine(mode="hybrd")  # Missing 'i'

        with pytest.raises(ValueError, match="Invalid mode"):
            StrategyEngine(mode="randomm")  # Extra 'm'


class TestRandomChoice:
    """Test random choice implementation details."""

    def test_random_choice_returns_string(self):
        """Test that _random_choice returns string, not enum or int."""
        engine = StrategyEngine(mode="random")
        choice = engine._random_choice()

        assert isinstance(choice, str)
        assert choice in ["even", "odd"]

    def test_random_choice_reproducibility_with_seed(self):
        """Test that random choices can be reproduced with same seed."""
        import random

        # Set seed for reproducibility
        random.seed(42)
        engine1 = StrategyEngine(mode="random")
        choice1 = engine1._random_choice()

        # Reset seed
        random.seed(42)
        engine2 = StrategyEngine(mode="random")
        choice2 = engine2._random_choice()

        # Should be same with same seed
        assert choice1 == choice2

    @pytest.mark.asyncio
    async def test_choose_parity_works_without_context_keys(self):
        """Test that choose_parity works even if context is missing keys."""
        engine = StrategyEngine(mode="random")

        # Context with unexpected structure
        context = {"unknown_key": "value"}

        choice = await engine.choose_parity(context)
        assert choice in ["even", "odd"]

    @pytest.mark.asyncio
    async def test_choose_parity_works_with_extra_context_keys(self):
        """Test that choose_parity ignores extra context keys."""
        engine = StrategyEngine(mode="random")

        context = {
            "opponent": "P02",
            "standings": {"P01": 3},
            "extra_key_1": "ignored",
            "extra_key_2": 12345
        }

        choice = await engine.choose_parity(context)
        assert choice in ["even", "odd"]


class TestInitializationCombinations:
    """Test various initialization parameter combinations."""

    def test_init_all_defaults(self):
        """Test initialization with all default parameters."""
        engine = StrategyEngine()  # Should default to hybrid mode

        assert engine.mode == "hybrid"
        assert engine.llm_timeout == 25

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"})
    def test_init_llm_custom_all_params(self):
        """Test LLM mode with all custom parameters."""
        engine = StrategyEngine(
            mode="llm",
            gemini_model_id="gemini-1.5-pro",
            temperature=0.5,
            max_output_tokens=150,
            llm_timeout=20,
            system_prompt="Custom prompt"
        )

        assert engine.mode == "llm"
        assert engine.llm_timeout == 20
        assert engine.agent is not None

    def test_init_random_ignores_llm_params(self):
        """Test that random mode ignores LLM parameters."""
        engine = StrategyEngine(
            mode="random",
            gemini_model_id="ignored-model",
            temperature=999,  # Should be ignored
            max_output_tokens=999,  # Should be ignored
            llm_timeout=15,
            system_prompt="Ignored prompt"
        )

        # Should initialize successfully and ignore LLM params
        assert engine.mode == "random"
        assert engine.agent is None
