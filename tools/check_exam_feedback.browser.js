(async()=>{
 const check=(ok,label)=>{if(!ok)throw Error(label);};
 const read=()=>JSON.parse(localStorage.getItem('framework-party-it0049-v1'));
 const question=s=>STUDY_DATA.questions.find(q=>q.id===s.queue[s.cursor]);
 const recordsBefore=JSON.stringify(read().records);
 let s=read().session;check(s.mode==='exam'&&s.queue.length===2,'Start an isolated two-question exam first.');
 const first=question(s),wrong=first.choices.find(c=>c!==first.answer);
 document.querySelector(`[data-option="${s.options[first.id].indexOf(wrong)}"]`).click();
 check(!document.querySelector('.answer-explanation'),'Exam must not reveal explanations after an answer.');
 check(!document.querySelector('.choice.correct,.choice.incorrect'),'Exam must not mark correct choices early.');
 check(JSON.stringify(read().records)===recordsBefore,'Exam grading waits for submission.');
 document.querySelector('[data-next]').click();s=read().session;const second=question(s);
 document.querySelector(`[data-option="${s.options[second.id].indexOf(second.answer)}"]`).click();
 check(!document.querySelector('.answer-explanation'),'No answer feedback before final submission.');
 document.querySelector('[data-next]').click();
 const reviews=[...document.querySelectorAll('.answer-explanation')];
 check(reviews.length===2,'Both exam answers have explanations.');
 check(reviews[0].querySelector('.answer-mistake').textContent.includes(first.choiceExplanations[wrong]),'Selected wrong answer receives its exact reason.');
 check(!reviews[1].querySelector('.answer-mistake'),'Correct answer is not described as wrong.');
 for(const [i,q]of [first,second].entries()){
  check(reviews[i].textContent.includes(q.explanation),'Correct answer reasoning appears.');
  check(reviews[i].querySelectorAll('[data-feedback-option]').length===3,'All three wrong choices receive explanations.');
  for(const option of q.choices.filter(c=>c!==q.answer))check(reviews[i].textContent.includes(q.choiceExplanations[option]),'Option reason remains matched after shuffling.');
 }
 check(read().session===null,'Submitted exam session closes.');
 check(read().records[first.id].lastCorrect===false&&read().records[second.id].lastCorrect===true,'The submitted grades are correct.');
 check(read().history[0].correct===1&&read().history[0].total===2,'The submitted score is 1/2.');
 return {passed:true,noEarlyFeedback:true,chosenMistakeExplained:true,allChoicesExplained:true,shuffledChoices:true,score:'1/2'};
})()
