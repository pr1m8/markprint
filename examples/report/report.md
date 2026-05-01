---
title: Architecture Report
author: Markprint
profile: report
theme: nord
toc: true
---

# Executive Summary

Markprint separates Markdown processing from PDF rendering.

# Architecture

Markdown becomes HTML, HTML becomes styled printable HTML, and then a renderer creates PDF bytes.
