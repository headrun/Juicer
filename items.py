# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class JuicerItem(Item):
    pass


class MovieItem(Item):
    sk                          = Field()
    title                       = Field()
    original_title              = Field()
    other_titles                 = Field()
    description                 = Field()
    genres                      = Field()
    sub_genres                  = Field()
    category                    = Field()
    duration                    = Field()
    languages                   = Field()
    original_languages          = Field()
    metadata_language           = Field()
    aka                         = Field()
    production_country          = Field()
    aux_info                    = Field()
    reference_url               = Field()
    avail_data                  = Field()       # This field is using only for vudu source


class TvshowItem(Item):
    sk                          = Field()
    title                       = Field()
    original_title              = Field()
    other_titles                 = Field()
    description                 = Field()
    genres                      = Field()
    sub_genres                  = Field()
    category                    = Field()
    duration                    = Field()
    languages                   = Field()
    original_languages          = Field()
    metadata_language           = Field()
    aka                         = Field()
    production_country          = Field()
    aux_info                    = Field()
    reference_url               = Field()
    avail_data                  = Field()       # This field is using only for vudu source


class SeasonItem(Item):
    sk                          = Field()
    tvshow_sk                   = Field()
    title                       = Field()
    original_title              = Field()
    other_titles                 = Field()
    description                 = Field()
    season_number               = Field()
    genres                      = Field()
    sub_genres                  = Field()
    category                    = Field()
    duration                    = Field()
    languages                   = Field()
    original_languages          = Field()
    metadata_language           = Field()
    aka                         = Field()
    production_country          = Field()
    aux_info                    = Field()
    reference_url               = Field()
    avail_data                  = Field()       # This field is using only for vudu source


class EpisodeItem(Item):
    sk                          = Field()
    season_sk                   = Field()
    tvshow_sk                   = Field()
    title                       = Field()
    show_title                  = Field()
    original_title              = Field()
    other_titles                  = Field()
    description                 = Field()
    episode_number              = Field()
    season_number               = Field()
    genres                      = Field()
    sub_genres                  = Field()
    category                    = Field()
    duration                    = Field()
    languages                   = Field()
    original_languages          = Field()
    metadata_language           = Field()
    aka                         = Field()
    production_country          = Field()
    aux_info                    = Field()
    reference_url               = Field()
    avail_data                  = Field()       # This field is using only for vudu source


class OtherMediaItem(Item):
    sk                          = Field()
    program_sk                  = Field()
    program_type                = Field()
    media_type                  = Field()
    title                       = Field()
    original_title              = Field()
    other_titles                = Field()
    description                 = Field()
    genres                      = Field()
    sub_genres                  = Field()
    category                    = Field()
    duration                    = Field()
    languages                   = Field()
    original_languages          = Field()
    metadata_language           = Field()
    aka                         = Field()
    production_country          = Field()
    aux_info                    = Field()
    reference_url               = Field()
    avail_data                  = Field()       # This field is using only for vudu source


class RelatedProgramItem(Item):
    program_sk      = Field()
    program_type    = Field()
    related_sk      = Field()
    related_rank    = Field()


class RichMediaItem(Item):
    sk            = Field()
    program_sk    = Field()
    program_type  = Field()
    media_type    = Field()
    image_type    = Field()
    size          = Field()
    dimensions    = Field()
    description   = Field()
    image_url     = Field()
    reference_url = Field()
    aux_info      = Field()


class RatingItem(Item):
    program_sk      = Field()
    program_type    = Field()
    rating          = Field()
    rating_type     = Field()
    rating_reason   = Field()


class PopularityItem(Item):
    program_sk      = Field()
    program_type    = Field()
    no_of_views     = Field()
    no_of_ratings   = Field()
    no_of_reviews   = Field()
    no_of_comments  = Field()
    no_of_likes     = Field()
    no_of_dislikes  = Field()
    aux_info        = Field()


class CrewItem(Item):
    sk               = Field()
    name             = Field()
    original_name    = Field()
    description      = Field()
    aka              = Field()
    gender           = Field()
    age              = Field()
    blood_group      = Field()
    birth_date       = Field()
    birth_place      = Field()
    death_date       = Field()
    death_place      = Field()
    constellation    = Field()
    country          = Field()
    occupation       = Field()
    biography        = Field()
    height           = Field()
    weight           = Field()
    rating           = Field()
    top_rated_works  = Field()
    no_of_ratings    = Field()
    family_members   = Field()
    recent_films     = Field()
    image            = Field()
    videos           = Field()
    reference_url    = Field()
    aux_info         = Field()


class ProgramCrewItem(Item):
    program_sk   = Field()
    program_type = Field()
    crew_sk      = Field()
    role         = Field()
    description  = Field()
    role_title   = Field()
    rank         = Field()
    aux_info     = Field()


class AwardsItem(Item):
    program_sk     = Field()
    program_type   = Field()
    award_name     = Field()
    award_category = Field()
    year           = Field()
    winner         = Field()
    winner_sk      = Field()
    winner_type    = Field()
    winner_flag    = Field()
    aux_info       = Field()


class ReleasesItem(Item):
    program_sk          = Field()
    program_type        = Field()
    company_name        = Field()
    region              = Field()
    relation            = Field()
    company_rights      = Field()
    release_date        = Field()
    release_year        = Field()
    country             = Field()
    studio              = Field()
    is_imax             = Field()
    is_giant_screens    = Field()
    aux_info            = Field()


class NewsItem(Item):
    sk            = Field()
    program_sk    = Field()
    program_type  = Field()
    title         = Field()
    description   = Field()
    published_at  = Field()
    reference_url = Field()
    aux_info      = Field()


class AvailItem(Item):
    source_id                   = Field()
    program_sk                  = Field()
    source_availabilities       = Field()
    source_program_id_space     = Field()


class ChartItem(Item):
    program_sk              = Field()
    program_type            = Field()
    chart_type              = Field()
    program_rank            = Field()
    week_number             = Field()
    week_end_date           = Field()
    no_of_weeks             = Field()
    currency                = Field()
    present_week_units      = Field()
    total_units             = Field()
    present_week_spending   = Field()
    total_spending          = Field()
    market_share            = Field()
    reference_url           = Field()
    aux_info                = Field()


class BoxofficeItem(Item):
    program_sk              = Field()
    program_rank            = Field()
    weekend_gross           = Field()
    total_gross             = Field()
    opening_gross           = Field()
    top_ten_gross           = Field()
    avg_gross               = Field()
    currency                = Field()
    location                = Field()
    no_of_locations         = Field()
    gross_type              = Field()
    year                    = Field()
    month                   = Field()
    quarter                 = Field()
    date                    = Field()
    weekday                 = Field()
    day_number              = Field()
    week_number             = Field()
    tickets_sold            = Field()
    visitors                = Field()
    release_strategy        = Field()


class ReviewsItem(Item):
    program_sk              = Field()
    program_type            = Field()
    title                   = Field()
    reviewed_on             = Field()
    reviewed_by             = Field()
    rating                  = Field()
    review                  = Field()
    review_url              = Field()


class TheaterItem(Item):
    sk                      = Field()
    name                    = Field()
    screen                  = Field()
    location                = Field()
    firm_name               = Field()
    is_3d                   = Field()
    no_of_rooms             = Field()
    no_of_seats             = Field()
    contact_numbers         = Field()
    zipcode                 = Field()
    latitude                = Field()
    longitude               = Field()
    address                 = Field()
    theater_url             = Field()


class TheaterAvailabilityItem(Item):
    program_sk              = Field()
    program_type            = Field()
    theater_sk              = Field()
    show_time               = Field()
    ticket_booking_link     = Field()
    is_3d                   = Field()


class PrimetimeItem(Item):
    program_sk              = Field()
    program_type            = Field()
    program_title           = Field()
    report_date             = Field()
    scope                   = Field()
    viewers_count           = Field()
    market_share            = Field()
    reference_url           = Field()


class ProgramChartsItem(Item):
    program_sk              = Field()
    program_type            = Field()
    channel_sk              = Field()
    program_title           = Field()
    hour                    = Field()
    minute                  = Field()
    rank                    = Field()
    no_of_views             = Field()
    votes                   = Field()
    rating                  = Field()
    weekday                 = Field()
    week                    = Field()
    month                   = Field()
    year                    = Field()
    reference_url           = Field()


class ChannelItem(Item):
    sk                      = Field()
    title                   = Field()
    description             = Field()
    genres                  = Field()
    sub_genres              = Field()
    image                   = Field()
    timezone_offset         = Field()
    reference_url           = Field()


class ChannelChartsItem(Item):
    channel_sk                          = Field()
    chart_type                          = Field()
    daily_reach_count                   = Field()
    daily_reach_count_in_percentage     = Field()
    weekly_reach_count                  = Field()
    weekly_reach_count_in_percentage    = Field()
    avg_pp_weekly_viewing               = Field()
    share                               = Field()
    week                                = Field()
    month                               = Field()
    year                                = Field()
    reference_url                       = Field()


class ScheduleItem(Item):
    channel_sk              = Field()
    program_sk              = Field()
    program_type            = Field()
    start_datetime          = Field()
    duration                = Field()
    attributes              = Field()


class OtherLinksItem(Item):
    sk                      = Field()
    program_sk              = Field()
    program_type            = Field()
    url_type                = Field()
    url                     = Field()


class LocationItem(Item):
    sk                      = Field()
    country                 = Field()
    state                   = Field()
    region                  = Field()
    sub_region              = Field()
    zipcode                 = Field()
    other_id                = Field()
    reference_url           = Field()


class LineupItem(Item):
    channel_sk              = Field()
    location_sk             = Field()
    stream_quality          = Field()
    tuner_number            = Field()
