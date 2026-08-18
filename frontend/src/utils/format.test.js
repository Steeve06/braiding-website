import { describe, expect, it } from "vitest";
import { formatCategoryLabel, formatDuration, formatPrice } from "./format.js";

describe("formatDuration", () => {
  it("formats minutes only when under an hour", () => {
    expect(formatDuration(45)).toBe("45 min");
  });

  it("formats whole hours with no remainder", () => {
    expect(formatDuration(120)).toBe("2 hr");
  });

  it("formats hours and minutes together", () => {
    expect(formatDuration(150)).toBe("2 hr 30 min");
  });
});

describe("formatPrice", () => {
  it("formats a decimal string price as a rounded dollar amount", () => {
    expect(formatPrice("200.00")).toBe("$200");
  });
});

describe("formatCategoryLabel", () => {
  it("replaces underscores with spaces", () => {
    expect(formatCategoryLabel("Knotless_Braids")).toBe("Knotless Braids");
  });
});
