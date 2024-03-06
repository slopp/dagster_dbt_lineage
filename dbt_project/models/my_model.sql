select 
    * 
from {{ source("main", "raw") }}