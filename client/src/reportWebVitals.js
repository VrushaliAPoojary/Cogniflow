import reportWebVitals from "./reportWebVitals";

// Optional: log metrics to console
reportWebVitals(console.log);

// Or send metrics to analytics service
reportWebVitals(metric => {
  fetch("/analytics", {
    method: "POST",
    body: JSON.stringify(metric),
  });
});
