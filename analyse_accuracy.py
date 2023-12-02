from datasets import load_metric

bleu = load_metric("bleu")
txt = "Fixed multiple small memory leaks. Click events are handled by React DOM more reliably in mobile browsers, particularly in Mobile Safari. Input events are handled more reliably in IE 10 and IE 11; spurious events no longer fire when using a placeholder. React DOM now supports the `cite` and `profile` HTML attributes. React DOM now supports the `onAnimationStart`, `onAnimationEnd`, `onAnimationIteration`, `onTransitionEnd`, and `onInvalid` events. Support for `onLoad` has been added to `object` elements.", "input": [{"role": "system", "content": "Summarize diff logs with a commit message."}, {"role": "user", "content": "diff --git a/docs/_posts/2016-03-07-react-v15-rc1.md b/docs/_posts/2016-03-07-react-v15-rc1.md\nindex 3eb8fb296fcf..932ae0988700 100644\n--- a/docs/_posts/2016-03-07-react-v15-rc1.md\n+++ b/docs/_posts/2016-03-07-react-v15-rc1.md\n@@ -87,7 +87,6 @@ Each of these changes will continue to work as before with a new warning until t\n ### Notable bug fixes\n \n - Fixed multiple small memory leaks\n-- Click events are handled by React DOM more reliably in mobile browsers, particularly in Mobile Safari.\n - Input events are handled more reliably in IE 10 and IE 11; spurious events no longer fire when using a placeholder.\n - React DOM now supports the `cite` and `profile` HTML attributes.\n - React DOM now supports the `onAnimationStart`, `onAnimationEnd`, `onAnimationIteration`, `onTransitionEnd`, and `onInvalid` events. Support for `onLoad` has been added to `object` elements."
x = txt.split()
txt2 = "remove 15 rc1 changelog entry that was fixed in 0.14"
y = txt.split()
predictions = [[x]]
references = [[[y]]]

bleu.compute(predictions=predictions, references=references)
