"""
Unit Tests for StrategyEngine

Tests parity choice strategies including random, LLM, and hybrid modes.

Coverage Target: Key functionality of strategy.py
"""

import pytest
import asyncio
from my_project.agents.player.strategy import StrategyEngine, choose_parity_random


class TestStrategyEngine:
    """Test suite for StrategyEngine building block."""

    def test_initialization_random_mode(self):
        """Test StrategyEngine initialization with random mode."""
        engine = StrategyEngine(mode="random")

        assert engine.mode == "random"
        assert engine.agent is None  # No LLM agent for random mode

    def test_initialization_invalid_mode_raises_error(self):
        """Test that invalid mode raises ValueError."""
        with pytest.raises(ValueError, match="Invalid mode"):
            StrategyEngine(mode="invalid")

    def test_initialization_timeout_too_large_raises_error(self):
        """Test that llm_timeout >= 30 raises ValueError."""
        with pytest.raises(ValueError, match="must be < 30 seconds"):
            StrategyEngine(mode="hybrid", llm_timeout=30)

        with pytest.raises(ValueError, match="must be < 30 seconds"):
            StrategyEngine(mode="hybrid", llm_timeout=35)

    @pytest.mark.asyncio
    async def test_choose_parity_random_mode(self):
        """Test parity choice with random mode."""
        engine = StrategyEngine(mode="random")

        context = {
            "opponent": "P02",
            "standings": {"P01": 3, "P02": 6},
            "history": []
        }

        choice = await engine.choose_parity(context)

        # Should return either "even" or "odd"
        assert choice in ["even", "odd"]

    @pytest.mark.asyncio
    async def test_choose_parity_random_always_lowercase(self):
        """Test that random mode always returns lowercase."""
        engine = StrategyEngine(mode="random")
        context = {}

        # Test multiple times to ensure consistency
        for _ in range(10):
            choice = await engine.choose_parity(context)
            assert choice in ["even", "odd"]
            assert choice == choice.lower()

    @pytest.mark.asyncio
    async def test_choose_parity_distribution(self):
        """Test that random choices are distributed (rough check)."""
        engine = StrategyEngine(mode="random")
        context = {}

        # Generate 100 choices
        choices = []
        for _ in range(100):
            choice = await engine.choose_parity(context)
            choices.append(choice)

        # Should have both even and odd (statistically almost certain)
        assert "even" in choices
        assert "odd" in choices

        # Rough distribution check (30-70% range for 100 samples)
        even_count = choices.count("even")
        assert 30 <= even_count <= 70

    def test_random_choice_method_direct(self):
        """Test _random_choice method directly."""
        engine = StrategyEngine(mode="random")

        choice = engine._random_choice()
        assert choice in ["even", "odd"]

    @pytest.mark.asyncio
    async def test_choose_parity_convenience_function(self):
        """Test choose_parity_random convenience function."""
        choice = await choose_parity_random()
        assert choice in ["even", "odd"]


class TestHybridMode:
    """Test hybrid mode behavior (LLM with fallback)."""

    @pytest.mark.asyncio
    async def test_hybrid_mode_without_api_key_falls_back_to_random(self):
        """Test that hybrid mode falls back to random when API key missing."""
        # This will fail to initialize LLM agent, but should still work with random fallback
        engine = StrategyEngine(mode="hybrid")

        context = {"opponent": "P02"}

        # Should not crash, should return random choice
        choice = await engine.choose_parity(context)
        assert choice in ["even", "odd"]


class TestEdgeCases:
    """Test edge cases."""

    @pytest.mark.asyncio
    async def test_empty_context(self):
        """Test with empty context dictionary."""
        engine = StrategyEngine(mode="random")

        choice = await engine.choose_parity({})
        assert choice in ["even", "odd"]

    @pytest.mark.asyncio
    async def test_context_with_none_values(self):
        """Test with None values in context."""
        engine = StrategyEngine(mode="random")

        context = {
            "opponent": None,
            "standings": None,
            "history": None
        }

        choice = await engine.choose_parity(context)
        assert choice in ["even", "odd"]
