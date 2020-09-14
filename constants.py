# TODO(dmauldin): fill in the rest of the values for each of these
#                 possibly fetching from API and memoizing them
# TODO(dmauldin): create a Version class?  Version.Minecraft.1_12_2?

class Category:
    All = 0


class Game:
    Minecraft = 432


# section is really just a category root
class Section:
    Mods = 6
    Modpacks = 4471
    ResourcePacks = 12
    Worlds = 17


class Sort:
    Featured = 0
    Popularity = 1
    LastUpdated = 2
    Name = 3
    Author = 4
    TotalDownloads = 5
