import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import StyleCard from "./StyleCard.jsx";

const sampleStyle = {
  id: 1,
  name: "Knotless Braids (medium)",
  category: "Knotless_Braids",
  description: "One pack on boho offered",
  prep_required: "wash and undo hair",
  estimated_duration_minutes: 150,
  maintenance_guidelines: "always wear cap",
  starting_price: "200.00",
  hero_image: "http://127.0.0.1:8000/media/styles/IMG_5158.jpg",
  is_active: true,
};

describe("StyleCard", () => {
  it("renders the style name and formatted price", () => {
    render(<StyleCard style={sampleStyle} />);

    expect(
      screen.getByRole("heading", { name: "Knotless Braids (medium)" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Starting at $200")).toBeInTheDocument();
  });

  it("renders the formatted category label and duration", () => {
    render(<StyleCard style={sampleStyle} />);

    expect(screen.getByText("Knotless Braids")).toBeInTheDocument();
    expect(screen.getByText("2 hr 30 min")).toBeInTheDocument();
  });
});
