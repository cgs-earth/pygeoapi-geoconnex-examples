library(httr)
library(sf)
library(readr)
library(tidyr)
library(dplyr)

url_geojson <- "https://www.sciencebase.gov/catalog/file/get/60be0e53d34e86b93891012b?f=__disk__9b%2F05%2Fb0%2F9b05b0e75e91d1692adcb1c2398e75e751865023&allowOpen=true"
gfv2 <- sf::read_sf(url_geojson)

url_csv <- "https://www.sciencebase.gov/catalog/file/get/60be0e53d34e86b93891012b?f=__disk__88%2Fbe%2F47%2F88be47f9e53f44eda6fdb8f1e4e0c79f85e33d06"
types <- readr::read_csv(url_csv)
nid_addressed <- dplyr::filter(types, !is.na(Type_NID))

# nid_url <- "https://nid.usace.army.mil/api/nation/csv"
# nid_csv <- readr::read_csv(nid_url)

base_url <- "https://nid.usace.army.mil/api/query?sy=%40stateKey%3A"

url_end <- "&addProps=yearsModified,conditionAssessId,conditionAssessDate,submitDate&out=csv"

# states <- sf::read_sf("https://reference.geoconnex.us/collections/states/items?limit=100&f=json")
# st <- states$STUSPS
# 
# 
# i <- st[1]
# url <- paste0(base_url,i,url_end)
# c <- readr::read_csv(url,col_types = cols(.default = "c"))
# c <- c[0,]
# 
# for(i in st){
#   url <- paste0(base_url,i,url_end)
#   c2 <- readr::read_csv(url,col_types = cols(.default = "c"))
#   c <-dplyr::bind_rows(c,c2)
# }

#write_csv(c,"../data/nid.csv")

nid <- readr::read_csv("data/nid.csv")
nid_ids <- 

nid_addressed <- nid_addressed %>% separate_rows(Type_NID, sep=" ")

psuedocode:
  
  for each nid_id, use NID API /suggestions endpoint to search for the id, add it to nid dataframe



