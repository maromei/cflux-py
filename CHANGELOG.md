# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-12

### Added

- `nothing` singleton to use instead of `Nothing()` in function definitions
    - Before:
        ```python
        from cflowpy import Option, Nothing
        # f.e. pyright will complain with the 'reportCallInDefaultInitializer' error
        def some_function(optional_value: Option[int] = Nothing()): ...
        ```
    - Now:
        ```python
        from cflowpy import Option, nothing
        def some_function(optional_value: Option[int] = nothing): ...
        ```
