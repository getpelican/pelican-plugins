(require 'json)
(require 'org)
(defun org->pelican (filename backend)
  (progn
    (save-excursion
      (find-file filename)
      (let ((properties (org-export-get-environment)))
        (princ (json-encode 
                (list 
                 :date (org-timestamp-format (car (plist-get properties :date)) "%Y-%m-%d")
                 :author (substring-no-properties (car (plist-get properties :author)))
                 :category (cdr (assoc "CATEGORY" org-file-properties))
                 :post (org-export-as backend nil nil t)
                 :title (substring-no-properties (car (plist-get properties :title))))))))))
