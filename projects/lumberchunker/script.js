// Embedded quiz data with multiple choice options
const QUIZ_DATA = {
  passage: [
    '"What about a story?" I said.',
    '"Could you very sweetly tell Winnie-the-Pooh one?"',
    '"I suppose I could," I said. "What sort of stories does he like?"',
    '"About himself. Because he\'s that sort of Bear."',
    '"Oh, I see."',
    '"So could you very sweetly?"',
    '"I\'ll try," I said.',
    'So I tried.',
    'Once upon a time, a very long time ago now, about last Friday, Winnie-the-Pooh lived in a forest all by himself under the name of Sanders.',
    '"What does \'under the name\' mean?" asked Christopher Robin.'
  ],
  question: "How should this passage be segmented for optimal semantic chunking?",
  options: [
    {
      id: 'A',
      label: 'Split after every sentence (10 chunks)',
      breaks: [0, 1, 2, 3, 4, 5, 6, 7, 8],
      chunks: [
        { sentences: [0], name: "Chunk 1" },
        { sentences: [1], name: "Chunk 2" },
        { sentences: [2], name: "Chunk 3" },
        { sentences: [3], name: "Chunk 4" },
        { sentences: [4], name: "Chunk 5" },
        { sentences: [5], name: "Chunk 6" },
        { sentences: [6], name: "Chunk 7" },
        { sentences: [7], name: "Chunk 8" },
        { sentences: [8], name: "Chunk 9" },
        { sentences: [9], name: "Chunk 10" }
      ],
      feedback: "This creates too many tiny chunks! Each sentence is isolated, losing the semantic connections between related dialogue. This approach would make retrieval inefficient and fail to capture the conversational flow."
    },
    {
      id: 'B',
      label: 'Keep everything together (1 chunk)',
      breaks: [],
      chunks: [
        { sentences: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name: "Entire Passage" }
      ],
      feedback: "This treats the entire passage as one chunk, mixing two distinct sections: the dialogue setup and the story beginning. The shift from meta-conversation to storytelling represents a clear semantic boundary that should be captured."
    },
    {
      id: 'C',
      label: 'Split between dialogue and story (2 chunks)',
      breaks: [7],
      chunks: [
        {
          sentences: [0, 1, 2, 3, 4, 5, 6, 7],
          name: "Dialogue Setup",
          reasoning: "These sentences form a complete dialogue where Christopher Robin asks for a story about Winnie-the-Pooh. They establish the context and setup for what follows, showing the conversational flow from request to agreement."
        },
        {
          sentences: [8, 9],
          name: "Story Beginning",
          reasoning: "These sentences transition from the setup dialogue into the actual storytelling. The narrator begins the story with a classic fairy tale opening, immediately followed by Christopher Robin's interruption with a question about the story."
        }
      ],
      feedback: "Correct! This segmentation recognizes the semantic boundary between the meta-dialogue (discussing what story to tell) and the actual storytelling. The first chunk captures the complete request-and-agreement exchange, while the second chunk begins the narrative with its classic opening and immediate interruption.",
      isCorrect: true
    }
  ],
  correctAnswer: 'C'
};

class TextChunkingQuiz {
  constructor() {
    this.quizData = QUIZ_DATA;
    this.selectedOption = null;
    this.hasSubmitted = false;
    this.init();
  }

  init() {
    this.renderProgressIndicator();
    this.renderQuiz();
    this.setupEventListeners();
  }

  renderProgressIndicator() {
    const container = d3.select('#progressIndicator');

    // Create SVG for progress indicator
    const width = 300;
    const height = 8;

    const svg = container.append('svg')
      .attr('width', width)
      .attr('height', height)
      .style('display', 'block')
      .style('margin', '0 auto');

    // Background track
    svg.append('rect')
      .attr('width', width)
      .attr('height', height)
      .attr('rx', 4)
      .attr('fill', '#e0e0e0');

    // Progress bar
    this.progressBar = svg.append('rect')
      .attr('width', 0)
      .attr('height', height)
      .attr('rx', 4)
      .attr('fill', '#464646');
  }

  updateProgress(percent) {
    if (!this.progressBar) return;

    const width = 300;
    this.progressBar
      .transition()
      .duration(500)
      .ease(d3.easeCubicOut)
      .attr('width', width * percent);
  }

  renderQuiz() {
    this.renderPassage();
    this.renderOptions();
  }

  renderPassage() {
    const container = d3.select('#passageContainer');

    // Remove loading text
    container.selectAll('.loading').remove();

    // Use d3 data join pattern
    const sentences = container.selectAll('.passage-sentence')
      .data(this.quizData.passage);

    // Enter new sentences
    sentences.enter()
      .append('p')
      .attr('class', 'passage-sentence')
      .attr('data-id', (d, i) => i)
      .style('opacity', 0)
      .style('transform', 'translateY(20px)')
      .text(d => d)
      .transition()
      .duration(600)
      .delay((d, i) => i * 80)
      .style('opacity', 1)
      .style('transform', 'translateY(0)');

    // Remove old sentences
    sentences.exit()
      .transition()
      .duration(300)
      .style('opacity', 0)
      .remove();
  }

  highlightPassageChunks(optionData) {
    // Clear all existing chunk classes
    d3.selectAll('.passage-sentence')
      .attr('class', 'passage-sentence');

    if (!optionData) return;

    // Apply chunk highlighting based on selected option
    optionData.chunks.forEach((chunk, chunkIndex) => {
      chunk.sentences.forEach(sentenceIdx => {
        d3.select(`.passage-sentence[data-id="${sentenceIdx}"]`)
          .classed(`chunk-${(chunkIndex % 5) + 1}`, true)
          .transition()
          .duration(400)
          .style('transform', 'scale(1.02)')
          .transition()
          .duration(200)
          .style('transform', 'scale(1)');
      });
    });
  }

  renderOptions() {
    const container = d3.select('#optionsContainer');

    // Remove loading text
    container.selectAll('.loading').remove();

    // Use d3 data join pattern
    const options = container.selectAll('.option-card')
      .data(this.quizData.options, d => d.id);

    // Exit old options
    options.exit()
      .transition()
      .duration(300)
      .style('opacity', 0)
      .remove();

    // Enter new options
    const optionsEnter = options.enter()
      .append('div')
      .attr('class', 'option-card')
      .attr('data-option-id', d => d.id)
      .style('opacity', 0)
      .style('transform', 'scale(0.95)')
      .on('click', (event, d) => this.selectOption(d.id));

    // Animate entrance
    optionsEnter
      .transition()
      .duration(500)
      .delay((d, i) => 800 + i * 150)
      .style('opacity', 1)
      .style('transform', 'scale(1)');

    // Build option structure
    const header = optionsEnter.append('div')
      .attr('class', 'option-header');

    header.append('input')
      .attr('type', 'radio')
      .attr('name', 'chunking-option')
      .attr('id', d => `option-${d.id}`)
      .attr('value', d => d.id)
      .property('checked', d => this.selectedOption === d.id);

    header.append('label')
      .attr('for', d => `option-${d.id}`)
      .html(d => `<strong>Option ${d.id}:</strong> ${d.label}`);

    // Update existing options (if any)
    options.classed('selected', d => this.selectedOption === d.id);
  }

  selectOption(optionId) {
    // Allow selection change at any time
    this.selectedOption = optionId;

    // Update progress to 50% when option selected
    this.updateProgress(0.5);

    // Get the selected option data and highlight passage
    const selectedOptionData = this.quizData.options.find(opt => opt.id === optionId);
    this.highlightPassageChunks(selectedOptionData);

    // Update visual selection with smooth transition
    d3.selectAll('.option-card')
      .transition()
      .duration(300)
      .style('border-color', function () {
        return d3.select(this).attr('data-option-id') === optionId ? '#464646' : '#e0e0e0';
      })
      .style('background-color', function () {
        return d3.select(this).attr('data-option-id') === optionId ? '#f8f9fa' : 'white';
      })
      .style('box-shadow', function () {
        return d3.select(this).attr('data-option-id') === optionId ?
          '0 4px 12px rgba(70,70,70,0.15)' : 'none';
      });

    d3.selectAll('.option-card')
      .classed('selected', false);
    d3.select(`.option-card[data-option-id="${optionId}"]`)
      .classed('selected', true);

    // Update radio button with animation
    d3.selectAll('input[name="chunking-option"]')
      .property('checked', false)
      .transition()
      .duration(200);

    d3.select(`#option-${optionId}`)
      .property('checked', true)
      .transition()
      .duration(200)
      .style('transform', 'scale(1.1)')
      .transition()
      .duration(200)
      .style('transform', 'scale(1)');

    // If already submitted, automatically resubmit with new selection
    if (this.hasSubmitted) {
      this.hasSubmitted = false;
      this.submitAnswer();
    }
  }

  setupEventListeners() {
    const submitBtn = d3.select('#submitBtn');

    // Click animation
    submitBtn.on('click', () => {
      // Pulse animation on click
      submitBtn
        .transition()
        .duration(100)
        .style('transform', 'scale(0.95)')
        .transition()
        .duration(100)
        .style('transform', 'scale(1)');

      this.submitAnswer();
    });

    // Hover effects
    submitBtn.on('mouseenter', function () {
      d3.select(this)
        .transition()
        .duration(200)
        .style('transform', 'translateY(-2px) scale(1.02)');
    });

    submitBtn.on('mouseleave', function () {
      d3.select(this)
        .transition()
        .duration(200)
        .style('transform', 'translateY(0) scale(1)');
    });
  }

  submitAnswer() {
    if (!this.selectedOption) {
      // Show error message with d3 animation
      const submitBtn = d3.select('#submitBtn');

      submitBtn
        .transition()
        .duration(100)
        .style('background-color', '#e57373')
        .style('border-color', '#e57373')
        .transition()
        .duration(100)
        .style('background-color', '#464646')
        .style('border-color', '#464646')
        .transition()
        .duration(100)
        .style('background-color', '#e57373')
        .style('border-color', '#e57373')
        .transition()
        .duration(100)
        .style('background-color', '#464646')
        .style('border-color', '#464646');

      alert('Please select an option before submitting!');
      return;
    }

    if (this.hasSubmitted) return; // Already submitted

    // Update progress to 100% on submit
    this.updateProgress(1.0);

    // Success animation on selected card
    const selectedCard = d3.select(`.option-card[data-option-id="${this.selectedOption}"]`);
    selectedCard
      .transition()
      .duration(200)
      .style('transform', 'scale(1.03)')
      .transition()
      .duration(200)
      .style('transform', 'scale(1)');

    this.hasSubmitted = true;
    this.showResults();
  }

  showResults() {
    const resultsContainer = d3.select('#resultsContainer');
    const quizContent = d3.select('.quiz-content');
    const controls = d3.select('.controls');

    // Fade out quiz with d3 transition
    quizContent
      .transition()
      .duration(400)
      .style('opacity', 0);

    controls
      .transition()
      .duration(400)
      .style('opacity', 0);

    setTimeout(() => {
      quizContent.classed('hidden', true);
      controls.classed('hidden', true);

      // Clear and build results
      resultsContainer.selectAll('*').remove();

      // Trigger resize after clearing
      if (window.sendHeightToParent) {
        window.sendHeightToParent();
      }

      const selectedOptionData = this.quizData.options.find(opt => opt.id === this.selectedOption);
      const isCorrect = selectedOptionData.isCorrect || false;

      // Result header with animation
      const header = resultsContainer.append('div')
        .attr('class', `result-header ${isCorrect ? 'correct' : 'incorrect'}`)
        .style('opacity', 0)
        .style('transform', 'translateY(-20px)');

      header.append('h2')
        .text(isCorrect ? 'Correct!' : 'Not Quite');

      header.append('p')
        .text(isCorrect ?
          'You identified the optimal semantic segmentation!' :
          'Let\'s review why this segmentation isn\'t ideal.');

      // Animate header entrance
      header.transition()
        .duration(600)
        .style('opacity', 1)
        .style('transform', 'translateY(0)')
        .on('end', () => {
          if (window.sendHeightToParent) {
            window.sendHeightToParent();
          }
        });

      // Show selected answer with data-driven approach
      const selectedSection = resultsContainer.append('div')
        .attr('class', 'result-section')
        .style('opacity', 0);

      selectedSection.append('h3')
        .html(`Your Answer: <span class="option-label">Option ${this.selectedOption}</span>`);

      selectedSection.append('div')
        .attr('class', 'feedback-box')
        .html(selectedOptionData.feedback);

      // Animate section entrance
      selectedSection
        .transition()
        .duration(600)
        .delay(300)
        .style('opacity', 1)
        .on('end', () => {
          if (window.sendHeightToParent) {
            window.sendHeightToParent();
          }
        });

      // Show selected option's chunks using data binding
      const chunksDiv = selectedSection.append('div')
        .attr('class', 'chunks-display');

      const chunks = chunksDiv.selectAll('.chunk-display')
        .data(selectedOptionData.chunks);

      const chunksEnter = chunks.enter()
        .append('div')
        .attr('class', 'chunk-display')
        .style('opacity', 0)
        .style('transform', 'translateY(20px)');

      chunksEnter.append('h4')
        .text(d => d.name);

      const sentencesDiv = chunksEnter.append('div')
        .attr('class', 'chunk-sentences');

      chunksEnter.each((chunk, idx, nodes) => {
        const chunkNode = d3.select(nodes[idx]);
        const sentencesContainer = chunkNode.select('.chunk-sentences');

        const sentences = sentencesContainer.selectAll('.chunk-sentence')
          .data(chunk.sentences);

        sentences.enter()
          .append('p')
          .attr('class', `chunk-sentence chunk-${(idx % 5) + 1}`)
          .text(sentenceIdx => this.quizData.passage[sentenceIdx])
          .style('opacity', 0)
          .transition()
          .duration(400)
          .delay((d, i) => 900 + idx * 200 + i * 100)
          .style('opacity', 1);

        if (chunk.reasoning) {
          chunkNode.append('div')
            .attr('class', 'reasoning-box')
            .html(`<strong>Why these belong together:</strong><br>${chunk.reasoning}`)
            .style('opacity', 0)
            .transition()
            .duration(400)
            .delay(1200 + idx * 200)
            .style('opacity', 1);
        }
      });

      // Animate chunks
      chunksEnter
        .transition()
        .duration(500)
        .delay((d, i) => 600 + i * 150)
        .style('opacity', 1)
        .style('transform', 'translateY(0)')
        .on('end', () => {
          if (window.sendHeightToParent) {
            window.sendHeightToParent();
          }
        });

      // If wrong, show correct answer
      if (!isCorrect) {
        const correctSection = resultsContainer.append('div')
          .attr('class', 'result-section correct-answer-section')
          .style('opacity', 0)
          .style('transform', 'scale(0.95)');

        correctSection.append('h3')
          .html(`Correct Answer: <span class="option-label">Option ${this.quizData.correctAnswer}</span>`);

        const correctOption = this.quizData.options.find(opt => opt.id === this.quizData.correctAnswer);

        correctSection.append('div')
          .attr('class', 'feedback-box correct-feedback')
          .html(correctOption.feedback);

        // Show correct chunks using data binding
        const correctChunksDiv = correctSection.append('div')
          .attr('class', 'chunks-display');

        const correctChunks = correctChunksDiv.selectAll('.chunk-display')
          .data(correctOption.chunks);

        const correctChunksEnter = correctChunks.enter()
          .append('div')
          .attr('class', 'chunk-display');

        correctChunksEnter.append('h4')
          .text(d => d.name);

        correctChunksEnter.append('div')
          .attr('class', 'chunk-sentences');

        correctChunksEnter.each((chunk, idx, nodes) => {
          const chunkNode = d3.select(nodes[idx]);
          const sentencesContainer = chunkNode.select('.chunk-sentences');

          const sentences = sentencesContainer.selectAll('.chunk-sentence')
            .data(chunk.sentences);

          sentences.enter()
            .append('p')
            .attr('class', `chunk-sentence chunk-${(idx % 5) + 1}`)
            .text(sentenceIdx => this.quizData.passage[sentenceIdx]);

          if (chunk.reasoning) {
            chunkNode.append('div')
              .attr('class', 'reasoning-box')
              .html(`<strong>Why these belong together:</strong><br>${chunk.reasoning}`);
          }
        });

        // Animate correct section
        correctSection
          .transition()
          .duration(700)
          .delay(1500)
          .style('opacity', 1)
          .style('transform', 'scale(1)')
          .on('end', () => {
            if (window.sendHeightToParent) {
              window.sendHeightToParent();
            }
          });
      }

      // Back button with animation
      const backButton = resultsContainer.append('div')
        .attr('class', 'action-buttons')
        .style('margin-top', '30px')
        .style('text-align', 'center')
        .style('opacity', 0);

      backButton.append('button')
        .attr('class', 'btn back-btn')
        .text('← Back to Quiz')
        .on('click', () => this.hideResults());

      backButton
        .transition()
        .duration(500)
        .delay(2000)
        .style('opacity', 1);

      // Show results with fade in
      resultsContainer.classed('show', true);

      // Trigger resize when results become visible and scroll to top
      if (window.sendHeightToParent) {
        window.sendHeightToParent(true);
      }

      setTimeout(() => {
        resultsContainer
          .transition()
          .duration(400)
          .style('opacity', 1)
          .on('end', () => {
            if (window.sendHeightToParent) {
              window.sendHeightToParent();
            }
          });
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400);
  }

  hideResults() {
    const resultsContainer = d3.select('#resultsContainer');
    const quizContent = d3.select('.quiz-content');
    const controls = d3.select('.controls');

    // Reset selection state
    this.selectedOption = null;
    this.hasSubmitted = false;

    // Reset progress to 0
    this.updateProgress(0);

    // Fade out results with d3 transition
    resultsContainer
      .transition()
      .duration(400)
      .style('opacity', 0);

    setTimeout(() => {
      resultsContainer.classed('show', false);

      // Clear passage highlighting
      this.highlightPassageChunks(null);

      // Deselect all options
      d3.selectAll('.option-card')
        .classed('selected', false)
        .style('border-color', '#e0e0e0')
        .style('background-color', 'white')
        .style('box-shadow', 'none');

      // Uncheck all radio buttons
      d3.selectAll('input[name="chunking-option"]')
        .property('checked', false);

      // Show quiz
      quizContent.classed('hidden', false).style('opacity', 0);
      controls.classed('hidden', false).style('opacity', 0);

      // Scroll to top first, before resizing
      if (window.sendHeightToParent) {
        window.sendHeightToParent(true);
      }

      setTimeout(() => {
        // Fade in quiz with staggered animation
        quizContent
          .transition()
          .duration(500)
          .style('opacity', 1);

        controls
          .transition()
          .duration(500)
          .delay(200)
          .style('opacity', 1);

        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 50);
    }, 400);
  }
}

// Initialize quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new TextChunkingQuiz();
});

