/*
 * SPDX-FileCopyrightText: 2026 Tokimi Rover contributors
 * SPDX-License-Identifier: Apache-2.0
 */

(() => {
  "use strict";

  const root = document.documentElement;
  const languageOptions = document.querySelectorAll("[data-language]");
  const yearTarget = document.querySelector("[data-current-year]");
  const signalStage = document.querySelector(".signal-stage");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  const readStoredLanguage = () => {
    try {
      return window.localStorage.getItem("tokimi-language");
    } catch {
      return null;
    }
  };

  const storeLanguage = (language) => {
    try {
      window.localStorage.setItem("tokimi-language", language);
    } catch {
      // The language switch still works when storage is disabled.
    }
  };

  const setLanguage = (language) => {
    const useEnglish = language === "en";
    root.classList.toggle("is-en", useEnglish);
    root.lang = useEnglish ? "en" : "zh-Hant";

    languageOptions.forEach((option) => {
      const isActive = option.dataset.language === (useEnglish ? "en" : "zh-Hant");
      option.setAttribute("aria-pressed", String(isActive));
    });
  };

  setLanguage(readStoredLanguage() === "en" ? "en" : "zh-Hant");

  languageOptions.forEach((option) => {
    option.addEventListener("click", () => {
      const nextLanguage = option.dataset.language;
      setLanguage(nextLanguage);
      storeLanguage(nextLanguage);
    });
  });

  if (yearTarget) {
    yearTarget.textContent = String(new Date().getFullYear());
  }

  const revealTargets = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || reduceMotion.matches) {
    revealTargets.forEach((target) => target.classList.add("is-visible"));
  } else {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) {
            return;
          }
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );

    revealTargets.forEach((target) => revealObserver.observe(target));
  }

  const updateSignalOffset = (event) => {
    if (!signalStage || reduceMotion.matches) {
      return;
    }

    const bounds = signalStage.getBoundingClientRect();
    const relativeX = (event.clientX - bounds.left) / bounds.width - 0.5;
    const relativeY = (event.clientY - bounds.top) / bounds.height - 0.5;
    root.style.setProperty("--shift-x", `${relativeX * 8}px`);
    root.style.setProperty("--shift-y", `${relativeY * 8}px`);
  };

  if (window.matchMedia("(pointer: fine)").matches) {
    signalStage?.addEventListener("pointermove", updateSignalOffset, { passive: true });
    signalStage?.addEventListener("pointerleave", () => {
      root.style.setProperty("--shift-x", "0px");
      root.style.setProperty("--shift-y", "0px");
    });
  }
})();
