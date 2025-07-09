document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('resumeForm');
  const resultBox = document.getElementById('resultBox');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const resumeFile = document.getElementById('resume').files[0];
    const jdText = document.getElementById('description').value.trim();

    if (!resumeFile || !jdText) {
      alert("Please upload a resume and enter a job description.");
      return;
    }

    try {
      // Upload Resume to Backend
      const formData = new FormData();
      formData.append('file', resumeFile);

      const resumeRes = await fetch('http://127.0.0.1:8000/upload-resume/', {
        method: 'POST',
        body: formData
      });

      if (!resumeRes.ok) throw new Error("Resume upload failed.");
      const resumeData = await resumeRes.json();

      const resumeText = resumeData.resume_text;

      // Match with JD
      const matchRes = await fetch('http://127.0.0.1:8000/match-resume/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });

      if (!matchRes.ok) throw new Error("Matching failed.");
      const matchData = await matchRes.json();

      // Show result in card
      resultBox.innerHTML = `
        <div class="card p-3 mt-3 bg-light border-success">
          <h4 class="text-success">Match Score: ${matchData.match_score_percent}%</h4>
          <p>${matchData.message}</p>
        </div>
      `;
      resultBox.style.display = 'block';

    } catch (err) {
      alert("Error: " + err.message);
      console.error(err);
    }
  });
});
