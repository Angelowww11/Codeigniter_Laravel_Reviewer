/* Explanations are matched to choice text, independently of shuffled positions. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.StudyFeedback=api;})(typeof window!=='undefined'?window:globalThis,()=>{
 'use strict';
 const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function render(q,chosen,{prose=escape,heading='h3'}={}){
  const h=heading==='h4'?'h4':'h3';
  const reason=option=>q.choiceExplanations?.[option]||'';
  const wrong=q.choices.includes(chosen)&&chosen!==q.answer;
  const others=q.choices.filter(option=>option!==q.answer&&(!wrong||option!==chosen));
  return `<section class="answer-explanation" aria-label="Answer explanation"><p class="answer-correct"><strong>Correct answer:</strong> ${prose(q.answer)}</p><${h}>Why this is correct</${h}><p data-correct-explanation>${prose(q.explanation)}</p>${wrong?`<div class="answer-mistake" data-feedback-option="${q.choices.indexOf(chosen)}"><${h}>Why your answer is wrong</${h}><p class="answer-chosen"><strong>${prose(chosen)}</strong></p><p>${prose(reason(chosen))}</p></div>`:chosen==='(unanswered)'?'<p class="answer-unanswered">You did not answer this question. Compare the choices with the explanation below.</p>':''}<${h}>${wrong?'Why the remaining choices are wrong':'Why the other choices are wrong'}</${h}><ul class="answer-alternatives">${others.map(option=>`<li data-feedback-option="${q.choices.indexOf(option)}"><p><strong>${prose(option)}</strong></p><p>${prose(reason(option))}</p></li>`).join('')}</ul></section>`;
 }
 return {render};
});
