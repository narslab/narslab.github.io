library("rcrossref")
library("yaml")
library("anytime")
library(stringr)
#setwd("papers/_posts/")
# dois <- c(
#           "10.1103/PhysRevLett.104.070402",
#           "10.1093/jamia/ocaa033",
#           "10.1177/0361198119853553",
#           "10.1007/s11116-020-10106-y",
#           "10.1088/1748-9326/ab22c7",
#           "10.1016/j.jth.2015.08.006",
#           "10.1007/s10479-016-2358-2",
#           "10.1007/s11067-018-9387-0",
#           "10.1016/j.cor.2015.02.010",
#           "10.1016/j.tra.2021.09.013",
#           "10.1038/s41598-021-01522-w",
#           "10.1016/j.tra.2020.06.013"
#           )

df = read.csv("../Publications.csv")
dois = df$DOI

#for(ii in 1:4) {
for(ii in 1:length(dois)) {
  #print(dois[ii])
  if (dois[ii] == "") {
      print(df[ii,]$Author)
      next
  }
  ## get doi reference with rcrossref:
  ref_md <- cr_cn(dois = dois[ii], format = "bibtex")
  #ref_md <- as.yaml(ref_md)
  ref_md <- unlist(strsplit(ref_md, "\n"))

  
  # layout  
  ref_layout <- "layout: paper"
  
  # title
  title <- str_extract(str_extract(ref_md, "title=\\{([^}]+)\\}"), "\\{([^}]+)\\}") #str_extract(grep("title=", ref_md, value = TRUE), "\\{(.*)\\}")
  title <- gsub("\\{|\\}", "", title)
  title_list <- unlist(strsplit(title, " "))
  ref_title <- paste0("title: ", "\"", title, "\"")
  
  # date
  date <- df[ii,]$Date
  print(date)
  date <- str_split(date,"-")[[1]]
  year <- date[1]
  month <- date[2]
  day <- date[3]
  if (is.na(month)) {
      month = "01"
  } 
  if (is.na(day)) {
      day = "01"
  } 
  
  #month <- gsub("\\{|\\}", "", str_extract(str_extract(ref_md, "month=\\{([^}]+)\\}"), "\\{([^}]+)\\}"))
  # month <- str_split(str_extract(ref_md, "month=([A-Za-z]{3})"), "=")[[1]][2] #, ",")[[1]][1]
  # if (length(month) > 0 ) {
  #     month <- str_which(month, fixed(month.abb, ignore_case = TRUE))
  #     if (month < 10) {
  #         month <- paste0("0", month)
  #     }
  # } else {
  #     month = "01"
  # }
  # 
  # day <- gsub("\\{|\\}", "", str_extract(str_extract(ref_md, "day=\\{([^}]+)\\}"), "\\{([^}]+)\\}"))
  # if (is.na(day)) {
  #     day = "01"
  # } else {
  #     if (length(day) > 0 ) {
  #         if (length(day) < 10 ) {
  #             day = paste0("0", day)
  #         }
  #     } else {
  #         day = "01"
  #     }
  # }
  
  # year <- gsub(",", "", unlist(strsplit(grep("year=", ref_md, value = TRUE), " "))[3])
  # year <- str_extract(str_extract(ref_md, "year=\\{([^}]+)\\}"), "\\{([^}]+)\\}")
  # year <- gsub("\\{|\\}", "", year)
  ref_year <- paste0("year: ", year)


  # authors 
  authors <- str_extract(str_extract(ref_md, "author=\\{([^}]+)\\}"), "\\{([^}]+)\\}")
  authors <- gsub("\\{|\\}", "", authors)
  authors <- gsub(" and", ",", authors)
  author_list <- unlist(strsplit(authors, ","))
  ref_authors <- paste0("authors: ", authors)
  
  # reference
  first_author_lastname <- tail(unlist(strsplit(author_list[1], " ")), n=1)
  if (length(author_list) > 2) {
    cit = paste0(first_author_lastname, " et al.")
  } else if (length(author_list) == 2) {
    second_author_lastname <- tail(unlist(strsplit(author_list[2], " "))[3], n=1)
    cit = paste0(first_author_lastname, " and ", second_author_lastname)
  } else {
    cit = first_author_lastname
  }
  journal <- str_extract(str_extract(ref_md, "journal=\\{([^}]+)\\}"), "\\{([^}]+)\\}")
  journal <- gsub("\\{|\\}", "", journal)
  #journal <- gsub("\\&", "and", journal)
  journal = gsub("\\$", "", journal)
  journal = gsub("\\&", "", journal)
  journal = gsub("\\\\", "", journal)
  journal = gsub("ampmathsemicolon", "and", journal)
  short_journal <- unlist(strsplit(journal, ":"))[1]
  ref_ref = paste0("ref: ", cit, " ", year, ". ", short_journal)
  
  # citation: journal/volume/number/pages
  volume <- gsub("\\{|\\}", "", str_extract(str_extract(ref_md, "volume=\\{([^}]+)\\}"), "\\{([^}]+)\\}"))
  number <- gsub("\\{|\\}", "", str_extract(str_extract(ref_md, "number=\\{([^}]+)\\}"), "\\{([^}]+)\\}"))
  
  pages <- gsub("\\{|\\}", "", str_extract(str_extract(ref_md, "pages=\\{([^}]+)\\}"), "\\{([^}]+)\\}"))
  pages <- gsub("--", "-", pages)
  
  if (length(number) != 0) {
    vol_num_pages = paste0(volume, "(", number, ")")
  } else {
    vol_num_pages = volume
  }
  if (length(pages) != 0) {
    vol_num_pages = paste0(vol_num_pages, ":", pages)
  }
  ref_journal <- paste0("journal: ", "\"", journal, " ", vol_num_pages, ".\"")
 
  # volume field
  ref_volume <- paste0("volume: ", volume)
  
  # doi
  doi <- str_extract(str_extract(ref_md, "DOI=\\{([^}]+)\\}"), "\\{([^}]+)\\}")
  doi <- gsub("\\{|\\}", "", doi)
  ref_doi <- paste0("doi: ", doi)
 
  ## make theme compliant *.md files from reference:
  ref_theme_md <- c(ref_layout, ref_title, ref_authors, ref_year, ref_ref, ref_journal, ref_volume, "pdf:", ref_doi, "github:")
  
  # abstract
  get_abstract <- function(doi) {
    tryCatch({
      abstract <- cr_abstract(doi)
      return(abstract)
      message("Successfully extracted abstract")
    },
    error = function(e) {
      message("Abstract not found. Original error message:")
      message(paste(e))
      return(character(0))
    },
    finally = {
      message("Contents of reference markdown completed")
    })
  }
  
  #abstract <- get_abstract(dois[ii])
  abstract <- df[ii, "Abstract.Note"] #jo
   
  if (length(abstract) > 0) {
    abstract <- gsub("Abstract", "", abstract, fixed = TRUE)
    ref_theme_md <- c("---", ref_theme_md, "---", "# Abstract", abstract)
  } else {
    ref_theme_md <- c("---", ref_theme_md, "---") 
  }
  
  ## format filename

  stopwords <- c("in", "for", "and", "a", "an", "the", "of", "on", "this", "to", "who", "whom", "whose", "why", "how", "where", "is", "my", "from")
  title_list <- tolower(title_list)
  title_list <- title_list[!title_list %in% stopwords]
  title_list <- title_list[1:3]
  title_list <- gsub("[[:punct:]]", "", title_list) # remove punctuation marks
  title_list <- paste(title_list, collapse = "-")
  
  
  filename = tolower(paste(year, month, day, first_author_lastname, title_list, sep = "-"))
  if (!file.exists(paste0("../papers/_posts/", filename, ".md"))) {
    write.table(ref_theme_md, file = paste0(filename, ".md"), #"./content/publications/",
                quote = FALSE, row.names = FALSE, col.names = FALSE)
    print(paste(ii, ":", dois[ii], "---", filename))
  }

}
