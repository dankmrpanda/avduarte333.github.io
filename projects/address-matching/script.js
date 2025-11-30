// Address Matching Challenge
// Based on "Improving Address Matching Using Siamese Transformer Networks"

// Portuguese address structure:
// [Artery Type] [Artery Name], [Door Number] [Door ID], [Accommodation ID], [ZIP CP4-CP3], [Postal Designation]

const GAME_DATA = [
  {
    unnormalized: "r doutor silva 45 2 esq 1000-201 lisboa",
    candidates: [
      // Score: 0.98 - Perfect match. All components align: artery type (Rua), name (Doutor Silva), 
      // door number (45), floor (2º), position (Esq), ZIP (1000-201), and city (Lisboa).
      // The bi-encoder recognizes "r" → "Rua" and "2 esq" → "2º Esq" as semantically identical.
      { text: "Rua Doutor Silva, 45 2º Esq, 1000-201, Lisboa", score: 0.98, isCorrect: true },
      
      // Score: 0.89 - Only the position differs (Dto vs Esq). The bi-encoder learned that 
      // Dto (direito/right) and Esq (esquerdo/left) are similar accommodation types but distinct.
      // High similarity because all other components match perfectly.
      { text: "Rua Doutor Silva, 45 2º Dto, 1000-201, Lisboa", score: 0.89, isCorrect: false },
      
      // Score: 0.85 - Door number differs (47 vs 45). The bi-encoder uses contextual embeddings
      // where nearby numbers have high similarity, but not identical. Two-digit difference
      // causes moderate penalty since door numbers are critical for exact matching.
      { text: "Rua Doutor Silva, 47 2º Esq, 1000-201, Lisboa", score: 0.85, isCorrect: false },
      
      // Score: 0.80 - Floor differs (1º vs 2º). Floor designation is semantically important
      // for address matching. The model learned that different floors are distinct locations,
      // resulting in lower similarity despite all other components matching.
      { text: "Rua Doutor Silva, 45 1º Esq, 1000-201, Lisboa", score: 0.80, isCorrect: false },
      
      // Score: 0.73 - Artery type differs (Avenida vs Rua). The bi-encoder learned that
      // Avenida (avenue) and Rua (street) are different street types. This is a significant
      // semantic difference, causing notable similarity drop despite other components matching.
      { text: "Avenida Doutor Silva, 45 2º Esq, 1000-201, Lisboa", score: 0.73, isCorrect: false }
    ]
  },
  {
    unnormalized: "av liberdade n 200 3 andar 1250-147 lx",
    candidates: [
      // Score: 0.95 - Perfect match. The bi-encoder successfully maps abbreviations:
      // "av" → "Avenida da", "n 200" → "200", "3 andar" → "3º", "lx" → "Lisboa".
      // The model learned that "da" articles are often omitted in unnormalized addresses.
      { text: "Avenida da Liberdade, 200 3º, 1250-147, Lisboa", score: 0.95, isCorrect: true },
      
      // Score: 0.88 - Floor differs (2º vs 3º). One floor difference causes moderate penalty.
      // The bi-encoder treats consecutive floors as semantically close but distinct locations,
      // maintaining high similarity while penalizing the mismatch.
      { text: "Avenida da Liberdade, 200 2º, 1250-147, Lisboa", score: 0.88, isCorrect: false },
      
      // Score: 0.84 - Door number differs (202 vs 200). Small numeric difference in door numbers
      // results in high but not perfect similarity. The transformer's positional encoding helps
      // it understand that 202 and 200 are nearby addresses on the same street.
      { text: "Avenida da Liberdade, 202 3º, 1250-147, Lisboa", score: 0.84, isCorrect: false },
      
      // Score: 0.78 - Missing article "da" in normalized form. While the bi-encoder learned
      // that articles are often optional, their complete absence in the normalized form
      // (which should be standardized) creates a structural mismatch, lowering similarity.
      { text: "Avenida Liberdade, 200 3º, 1250-147, Lisboa", score: 0.78, isCorrect: false },
      
      // Score: 0.70 - Artery type differs (Rua vs Avenida). This is a significant semantic
      // difference. The bi-encoder learned that Rua and Avenida represent different street
      // classifications, causing substantial similarity penalty despite other matches.
      { text: "Rua da Liberdade, 200 3º, 1250-147, Lisboa", score: 0.70, isCorrect: false }
    ]
  },
  {
    unnormalized: "travessa flores 12 rc direito 4000-220 porto",
    candidates: [
      // Score: 0.96 - Perfect match. The bi-encoder maps "travessa flores" → "Travessa das Flores"
      // (adding the article "das"), "rc direito" → "R/C Dto" (ground floor right), and
      // recognizes "porto" → "Porto". All semantic components align perfectly.
      { text: "Travessa das Flores, 12 R/C Dto, 4000-220, Porto", score: 0.96, isCorrect: true },
      
      // Score: 0.90 - Position differs (Esq vs Dto). Left vs right position is semantically
      // significant. The bi-encoder learned these are opposite sides of the same floor,
      // maintaining high similarity while recognizing they're distinct apartments.
      { text: "Travessa das Flores, 12 R/C Esq, 4000-220, Porto", score: 0.90, isCorrect: false },
      
      // Score: 0.83 - Floor differs (1º vs R/C). Ground floor (R/C) vs first floor (1º) is
      // a meaningful distinction. The bi-encoder treats adjacent floors as semantically close
      // but applies moderate penalty since they're different physical locations.
      { text: "Travessa das Flores, 12 1º Dto, 4000-220, Porto", score: 0.83, isCorrect: false },
      
      // Score: 0.77 - Missing article "das" in normalized form. The bi-encoder expects
      // normalized addresses to include proper articles. The absence creates a structural
      // inconsistency, though the core address components still match well.
      { text: "Travessa Flores, 12 R/C Dto, 4000-220, Porto", score: 0.77, isCorrect: false },
      
      // Score: 0.68 - Door number differs (14 vs 12). Two-number difference in door numbers
      // causes notable similarity drop. The bi-encoder learned that door numbers are critical
      // identifiers, and even small differences indicate potentially different buildings.
      { text: "Travessa das Flores, 14 R/C Dto, 4000-220, Porto", score: 0.68, isCorrect: false }
    ]
  },
  {
    unnormalized: "lg republica 8 1 frente 3000-343 coimbra",
    candidates: [
      // Score: 0.97 - Perfect match. The bi-encoder successfully decodes "lg" → "Largo da",
      // "1 frente" → "1º Fte" (first floor front), and all other components. The model
      // learned that "frente" and "Fte" are semantically equivalent position indicators.
      { text: "Largo da República, 8 1º Fte, 3000-343, Coimbra", score: 0.97, isCorrect: true },
      
      // Score: 0.89 - Position differs (Tras vs Fte). Front (Fte) vs back (Tras) position
      // is semantically significant. The bi-encoder learned these indicate opposite sides
      // of the building, maintaining high similarity while recognizing distinct locations.
      { text: "Largo da República, 8 1º Tras, 3000-343, Coimbra", score: 0.89, isCorrect: false },
      
      // Score: 0.85 - Floor differs (2º vs 1º). One floor difference causes moderate penalty.
      // The transformer's attention mechanism recognizes that consecutive floors share the
      // same building but are distinct addresses, balancing similarity and distinction.
      { text: "Largo da República, 8 2º Fte, 3000-343, Coimbra", score: 0.85, isCorrect: false },
      
      // Score: 0.78 - Door number differs (6 vs 8). Two-number difference in door numbers
      // creates moderate similarity drop. The bi-encoder treats nearby door numbers as
      // potentially related but distinct addresses, applying appropriate penalty.
      { text: "Largo da República, 6 1º Fte, 3000-343, Coimbra", score: 0.78, isCorrect: false },
      
      // Score: 0.72 - Artery type differs (Praça vs Largo). Both mean "square" but are
      // different classifications. The bi-encoder learned that Praça and Largo, while
      // semantically related, represent distinct street type categories in Portuguese.
      { text: "Praça da República, 8 1º Fte, 3000-343, Coimbra", score: 0.72, isCorrect: false }
    ]
  },
  {
    unnormalized: "prc comercio 25 loja a 1100-148 lx",
    candidates: [
      // Score: 0.94 - Perfect match. The bi-encoder decodes "prc" → "Praça do",
      // "loja a" → "Loja A" (shop A), and "lx" → "Lisboa". The model learned that
      // "Loja" indicates commercial ground-floor space, distinct from residential floors.
      { text: "Praça do Comércio, 25 Loja A, 1100-148, Lisboa", score: 0.94, isCorrect: true },
      
      // Score: 0.87 - Shop identifier differs (Loja B vs Loja A). Adjacent shop letters
      // indicate nearby commercial units. The bi-encoder maintains high similarity since
      // they're in the same building, but recognizes they're distinct commercial spaces.
      { text: "Praça do Comércio, 25 Loja B, 1100-148, Lisboa", score: 0.87, isCorrect: false },
      
      // Score: 0.84 - Door number differs (27 vs 25). Small numeric difference causes
      // moderate penalty. The bi-encoder learned that even-numbered addresses on squares
      // can be close but represent different buildings or entrances.
      { text: "Praça do Comércio, 27 Loja A, 1100-148, Lisboa", score: 0.84, isCorrect: false },
      
      // Score: 0.76 - Missing article "do" in normalized form. The bi-encoder expects
      // proper articles in normalized addresses. "Praça Comércio" vs "Praça do Comércio"
      // creates structural inconsistency, lowering similarity despite other matches.
      { text: "Praça Comércio, 25 Loja A, 1100-148, Lisboa", score: 0.76, isCorrect: false },
      
      // Score: 0.68 - Artery type differs (Largo vs Praça). Both mean "square" but are
      // different official classifications. The bi-encoder learned that Largo and Praça,
      // while semantically similar, represent distinct administrative street types.
      { text: "Largo do Comércio, 25 Loja A, 1100-148, Lisboa", score: 0.68, isCorrect: false }
    ]
  }
];

class BiEncoderGame {
  constructor() {
    this.currentRound = 0;
    this.userRanking = [];
    this.score = 0;
    this.totalRounds = Math.min(3, GAME_DATA.length); // Limit to 3 rounds
    this.init();
  }

  init() {
    this.loadRound();
    this.setupEventListeners();
  }

  loadRound() {
    const roundData = GAME_DATA[this.currentRound];
    
    // Display unnormalized address
    const unnormalizedDiv = document.getElementById('unnormalizedAddress');
    unnormalizedDiv.innerHTML = `<strong>${roundData.unnormalized}</strong>`;
    
    // Randomize candidate order
    const shuffledCandidates = roundData.candidates
      .map((candidate, originalIndex) => ({ ...candidate, originalIndex }))
      .sort(() => Math.random() - 0.5);
    
    // Display candidates in randomized order
    const candidatesContainer = document.getElementById('candidatesContainer');
    candidatesContainer.innerHTML = '';
    
    shuffledCandidates.forEach((candidate, displayIndex) => {
      const card = document.createElement('div');
      card.className = 'candidate-card';
      card.dataset.index = candidate.originalIndex; // Store original index for scoring
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: start;">
          <div style="flex: 1;">${candidate.text}</div>
        </div>
      `;
      
      card.addEventListener('click', () => this.selectCandidate(candidate.originalIndex));
      candidatesContainer.appendChild(card);
    });
    
    // Reset ranking display
    this.userRanking = [];
    this.updateRankingDisplay();
    document.getElementById('submitBtn').disabled = true;
  }

  selectCandidate(index) {
    const roundData = GAME_DATA[this.currentRound];
    const candidate = roundData.candidates[index];
    
    // Check if already selected
    const existingIndex = this.userRanking.findIndex(r => r.index === index);
    
    if (existingIndex !== -1) {
      // Deselect
      this.userRanking.splice(existingIndex, 1);
    } else {
      // Select (max 3)
      if (this.userRanking.length < 3) {
        this.userRanking.push({ index, text: candidate.text });
      } else {
        // Replace the last one
        this.userRanking[2] = { index, text: candidate.text };
      }
    }
    
    this.updateRankingDisplay();
    this.updateCandidateCards();
    
    // Enable submit button if 3 selected
    document.getElementById('submitBtn').disabled = this.userRanking.length !== 3;
  }

  updateRankingDisplay() {
    const rankingList = document.getElementById('rankingList');
    rankingList.innerHTML = '';
    
    for (let i = 0; i < 3; i++) {
      const slot = document.createElement('div');
      slot.className = 'rank-slot';
      slot.dataset.rank = i + 1;
      
      if (this.userRanking[i]) {
        slot.innerHTML = `${i + 1}. <span class="selected-address">${this.userRanking[i].text}</span>`;
      } else {
        slot.innerHTML = `${i + 1}. <span class="rank-placeholder">Click a candidate</span>`;
      }
      
      rankingList.appendChild(slot);
    }
  }

  updateCandidateCards() {
    const cards = document.querySelectorAll('.candidate-card');
    cards.forEach(card => {
      const index = parseInt(card.dataset.index);
      const isSelected = this.userRanking.some(r => r.index === index);
      
      if (isSelected) {
        card.classList.add('selected');
      } else {
        card.classList.remove('selected');
      }
    });
  }

  setupEventListeners() {
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.addEventListener('click', () => this.submitRanking());
    
    const nextRoundBtn = document.getElementById('nextRoundBtn');
    nextRoundBtn.addEventListener('click', () => this.nextRound());
    
    const resetBtn = document.getElementById('resetBtn');
    resetBtn.addEventListener('click', () => this.resetGame());
  }

  resetGame() {
    // Confirm before resetting
    if (confirm('Are you sure you want to reset the game? Your current progress will be lost.')) {
      // Reset all game state
      this.currentRound = 0;
      this.userRanking = [];
      this.score = 0;
      
      // Hide solution phase if visible
      const solutionPhase = document.getElementById('solutionPhase');
      const answerPhase = document.getElementById('answerPhase');
      solutionPhase.classList.remove('show');
      solutionPhase.style.display = 'none';
      answerPhase.style.display = 'flex';
      
      // Load first round
      this.loadRound();
    }
  }

  submitRanking() {
    if (this.userRanking.length !== 3) return;
    
    const roundData = GAME_DATA[this.currentRound];
    
    // Find correct answer
    const correctIndex = roundData.candidates.findIndex(c => c.isCorrect);
    const correctCandidate = roundData.candidates[correctIndex];
    
    // Check if user found the correct answer in top 3
    const userFoundCorrect = this.userRanking.some(r => r.index === correctIndex);
    
    // Get user's rank of the correct answer (0-indexed, or -1 if not found)
    const userCorrectRank = this.userRanking.findIndex(r => r.index === correctIndex);
    
    // Calculate score based on ranking position
    if (userFoundCorrect) {
      if (userCorrectRank === 0) {
        this.score += 3; // 3 points for ranking it #1
      } else if (userCorrectRank === 1) {
        this.score += 2; // 2 points for ranking it #2
      } else {
        this.score += 1; // 1 point for ranking it #3
      }
    }
    
    // Show results
    this.showResults(correctIndex, correctCandidate, userFoundCorrect, userCorrectRank);
  }

  showResults(correctIndex, correctCandidate, userFoundCorrect, userCorrectRank) {
    const answerPhase = document.getElementById('answerPhase');
    const solutionPhase = document.getElementById('solutionPhase');
    const solutionContent = document.getElementById('solutionContent');
    
    // Hide answer phase
    answerPhase.style.display = 'none';
    
    // Build results
    let html = '<div class="solution-content">';
    
    // Result header
    if (userFoundCorrect) {
      if (userCorrectRank === 0) {
        html += `
          <div class="result-header correct">
            <h3>🎉 Perfect!</h3>
            <p>You ranked the correct address #1! (+3 points)</p>
          </div>
        `;
      } else if (userCorrectRank === 1) {
        html += `
          <div class="result-header correct">
            <h3>✓ Great!</h3>
            <p>You ranked the correct address #2 (+2 points)</p>
          </div>
        `;
      } else {
        html += `
          <div class="result-header correct">
            <h3>✓ Good!</h3>
            <p>You found the correct address in your top 3 (+1 point)</p>
          </div>
        `;
      }
    } else {
      html += `
        <div class="result-header incorrect">
          <h3>Not Quite</h3>
          <p>The correct address wasn't in your top 3 (0 points)</p>
        </div>
      `;
    }
    
    // Show correct answer
    html += `
      <div class="feedback-box correct-feedback" style="margin-top: 15px;">
        <strong>Correct Match:</strong><br>
        ${correctCandidate.text}
        <br><br>
        <strong>Why this is correct:</strong> This normalized address exactly matches all components of the unnormalized input: artery type, artery name, door number, accommodation ID, and ZIP code.
      </div>
    `;
    
    // Show user's ranking
    html += '<div style="margin-top: 20px;"><h4 style="color: #464646; margin-bottom: 10px;">Your Ranking:</h4>';
    html += '<ul style="margin-top: 5px;">';
    this.userRanking.forEach((r, i) => {
      const isCorrect = r.index === correctIndex;
      const badge = isCorrect ? '<span class="candidate-badge badge-correct">CORRECT</span>' : '';
      html += `<li>${i + 1}. ${r.text} ${badge}</li>`;
    });
    html += '</ul></div>';
    
    // Score display
    html += `
      <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center;">
        <strong>Round ${this.currentRound + 1} of ${this.totalRounds}</strong><br>
        <span style="font-size: 1.2em; color: #464646;">Score: ${this.score} points</span>
      </div>
    `;
    
    html += '</div>';
    
    solutionContent.innerHTML = html;
    
    // Show solution phase
    solutionPhase.style.display = 'flex';
    setTimeout(() => {
      solutionPhase.classList.add('show');
    }, 50);
    
    // Update button text and visibility
    const nextBtn = document.getElementById('nextRoundBtn');
    nextBtn.style.display = 'block'; // Ensure button is visible for regular rounds
    if (this.currentRound < this.totalRounds - 1) {
      nextBtn.textContent = 'Next Round →';
    } else {
      nextBtn.textContent = 'See Final Score →';
    }
  }

  nextRound() {
    const solutionPhase = document.getElementById('solutionPhase');
    const answerPhase = document.getElementById('answerPhase');
    
    // Hide solution
    solutionPhase.classList.remove('show');
    setTimeout(() => {
      solutionPhase.style.display = 'none';
      
      // Check if game is over
      if (this.currentRound >= this.totalRounds - 1) {
        this.showFinalScore();
      } else {
        // Load next round
        this.currentRound++;
        this.loadRound();
        answerPhase.style.display = 'flex';
      }
    }, 400);
  }

  showFinalScore() {
    const solutionContent = document.getElementById('solutionContent');
    const maxScore = this.totalRounds * 3; // 3 points per round max
    const percentage = (this.score / maxScore * 100).toFixed(1);
    
    let message = '';
    if (percentage >= 80) {
      message = '🏆 Outstanding! You have a great eye for address matching!';
    } else if (percentage >= 60) {
      message = '👍 Good job! You understand the key patterns in address matching.';
    } else if (percentage >= 40) {
      message = '📚 Not bad! Address matching is tricky with subtle differences.';
    } else {
      message = '🤔 Address matching is harder than it looks! The bi-encoder uses semantic similarity to handle variations.';
    }
    
    const html = `
      <div class="solution-content">
        <div class="result-header correct">
          <h3>Game Complete!</h3>
          <p>${message}</p>
        </div>
        <div class="final-row" style="margin-top: 20px; align-items: center; justify-content: center;">
          <div class="final-score-box" style="padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center; min-width: 260px;">
            <div style="font-size: 2em; font-weight: bold; color: #464646; margin-bottom: 10px;">
              ${this.score} / ${maxScore}
            </div>
            <div style="font-size: 1.2em; color: #666;">
              ${percentage}% Accuracy
            </div>
          </div>
          <div class="final-actions" style="margin-left: 18px; display:flex; gap:10px; flex-direction:column;">
            <div style="display:flex; align-items:center; justify-content:center;">
              <button class="quiz-btn submit-btn final-play-btn" onclick="location.reload()" style="padding: 14px 26px;">Play Again</button>
            </div>
          </div>
        </div>
        <div class="feedback-box" style="margin-top: 20px;">
          <strong>About the Bi-Encoder:</strong><br>
          The bi-encoder uses Siamese Transformer networks to embed addresses into a semantic vector space. It computes cosine similarity between the query embedding and candidate embeddings, producing scores from 0 to 1. The system handles missing fields, reordered components, abbreviations, and typos by learning semantic similarity rather than relying on exact string matching. In production, it achieves 99.41% recall@10.
        </div>
      </div>
    `;
    
    solutionContent.innerHTML = html;
    
    // Hide the Next Round button on final score page
    const nextRoundBtn = document.getElementById('nextRoundBtn');
    if (nextRoundBtn) {
      nextRoundBtn.style.display = 'none';
    }
    
    const solutionPhase = document.getElementById('solutionPhase');
    solutionPhase.style.display = 'flex';
    setTimeout(() => {
      solutionPhase.classList.add('show');
    }, 50);
  }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new BiEncoderGame();
});
