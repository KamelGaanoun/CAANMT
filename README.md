# Explanation-Augmented Context-Aware Neural Machine Translation

This repository contains the code and data for the paper "Transformer Meets External Context: A Novel Approach to Enhance Neural Machine Translation" by Mohammed Alsuhaibani, Kamel Gaanoun, and Ali Alsohaibani.

## Introduction

In this work, we propose a novel approach to improve Neural Machine Translation (NMT) by incorporating external context, specifically explanations of the source text meanings. By leveraging state-of-the-art transformer-based models and techniques for context injection, we demonstrate significant improvements in translation quality, particularly for Arabic-to-English translation.

## Contributions

- A novel strategy to enhance NMT by incorporating contextual data extracted from source-specific explanatory materials.
- Fine-tuning a multilingual T5 model (mT5) using two newly proposed datasets: one with source content and translations, and another with source content enriched with relevant contextual details.
- Three different methods for context injection: using complete explanations, summarized explanations, and summarized explanations with an additional identifying detail.
- A curated Arabic-English parallel dataset, enriched with comprehensive explanations of the source text, facilitating research on context-aware NMT and contextual augmentation.

## Dataset

We introduce a new dataset composed of Arabic verses from the Quran, their English translations, and explanations (tafseer) derived from the Saadi Exegesis. The dataset is available in the `Data/` directory and is split into train, development, and test sets.

