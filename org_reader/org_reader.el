(require 'json)
(require 'org)
(require 'ox)
(require 'package)

;; htmlize is needed for SRC blocks
(setq package-load-list '((htmlize t)))
(package-initialize)

(defun org->pelican (filename backend)
  (progn
    (save-excursion
      ; open org file
      (find-file filename)

      ; pre-process some metadata
      (let (; extract org export properties
            (org-export-env (org-export-get-environment))
            ; convert MODIFIED prop to string
            (modifiedstr (cdr (assoc-string "MODIFIED" org-keyword-properties t)))
            ; prepare date property
            (dateobj (car (plist-get (org-export-get-environment) ':date))))

        ; check if #+TITLE: is given and give sensible error message if not
        (if (symbolp (car (plist-get org-export-env :title)))
            (error "Each page/article must have a #+TITLE: property"))

        ; construct the JSON object
        (princ (json-encode
                (list
                 ; org export environment
                 :title (substring-no-properties
                         (car (plist-get org-export-env :title)))
                 ; if #+DATE is not given, dateobj is nil
                 ; if #+DATE is a %Y-%m-%d string, dateobj is a string,
                 ; and otherwise we assume #+DATE is a org timestamp
                 :date (if (symbolp dateobj)
                           ""
                         (if (stringp dateobj)
                             (org-read-date nil nil dateobj nil)
                           (org-timestamp-format dateobj "%Y-%m-%d")))

                 :author (substring-no-properties
                          (car (plist-get org-export-env ':author)))

                 ; org file properties
                 :category (cdr (assoc-string "CATEGORY" org-keyword-properties t))

                 ; custom org file properties, defined as #+PROPERTY: NAME ARG
                 :language (cdr (assoc-string "LANGUAGE" org-keyword-properties t))
                 :save_as (cdr (assoc-string "SAVE_AS" org-keyword-properties t))
                 :tags (cdr (assoc-string "TAGS" org-keyword-properties t))
                 :template (cdr (assoc-string "TEMPLATE" org-keyword-properties t))
                 :summary (cdr (assoc-string "SUMMARY" org-keyword-properties t))
                 :status (cdr (assoc-string "STATUS" org-keyword-properties t))
                 :slug (cdr (assoc-string "SLUG" org-keyword-properties t))
                 :modified (if (stringp modifiedstr)
                               (org-read-date nil nil modifiedstr nil)
                             "")
                 :post (org-export-as backend nil nil t))))))))
