const askButton = document.getElementById("ask");
const questionInput = document.getElementById("question");
const statusLine = document.getElementById("status");
const answerBox = document.getElementById("answer");

askButton.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  answerBox.hidden = true;
  answerBox.textContent = "";
  if (question.length < 3) {
    statusLine.textContent = "Please enter a question of at least 3 characters.";
    return;
  }

  askButton.disabled = true;
  statusLine.textContent = "The agent team is preparing an educational response...";
  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");
    answerBox.textContent = data.answer + "\n\n" + data.disclaimer;
    answerBox.hidden = false;
    statusLine.textContent = "Response ready.";
  } catch (error) {
    statusLine.textContent = "Unable to get a response: " + error.message;
  } finally {
    askButton.disabled = false;
  }
});
