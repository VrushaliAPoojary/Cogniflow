import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "./App";

test("renders Workflow Builder page by default", () => {
  render(
    <MemoryRouter initialEntries={["/"]}>
      <App />
    </MemoryRouter>
  );

  const workflowHeading = screen.getByText(/components/i); // From ComponentPanel
  expect(workflowHeading).toBeInTheDocument();
});

test("navigates to Chat page", () => {
  render(
    <MemoryRouter initialEntries={["/chat"]}>
      <App />
    </MemoryRouter>
  );

  const chatHeading = screen.getByText(/chat/i);
  expect(chatHeading).toBeInTheDocument();
});
