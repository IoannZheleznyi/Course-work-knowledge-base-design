WITH search_input AS (
    SELECT translate(
        :query,
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
    ) AS normalized_query
),
matched_spices AS (
    SELECT
        s.id,
        s.name,
        s.slug,
        s.description,
        s.origin,
        s.usage,
        c.name AS category
    FROM spices s
    JOIN categories c ON c.id = s.category_id
    CROSS JOIN search_input q
    WHERE
        strpos(
            translate(
                s.name,
                'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
            ),
            q.normalized_query
        ) > 0
        OR strpos(
            translate(
                s.slug,
                'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
            ),
            q.normalized_query
        ) > 0
        OR strpos(
            translate(
                s.description,
                'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
            ),
            q.normalized_query
        ) > 0
)
SELECT
    jsonb_build_object(
        'id', ms.id,
        'name', ms.name,
        'slug', ms.slug,
        'description', ms.description,
        'origin', ms.origin,
        'usage', ms.usage,
        'category', ms.category,

        'articles', COALESCE(
            (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'id', a.id,
                        'title', a.title,
                        'description', a.description,
                        'content', a.content,
                        'source_name', a.source_name,
                        'source_url', a.source_url
                    )
                )
                FROM articles a
                WHERE a.spice_id = ms.id
            ),
            jsonb_build_array()
        ),

        'images', COALESCE(
            (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'id', i.id,
                        'title', i.title,
                        'description', i.description,
                        'image_url', i.image_url,
                        'source_url', i.source_url
                    )
                )
                FROM images i
                WHERE i.spice_id = ms.id
            ),
            jsonb_build_array()
        ),

        'videos', COALESCE(
            (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'id', v.id,
                        'title', v.title,
                        'description', v.description,
                        'video_url', v.video_url,
                        'source_name', v.source_name
                    )
                )
                FROM videos v
                WHERE v.spice_id = ms.id
            ),
            jsonb_build_array()
        )
    ) AS result
FROM matched_spices ms
ORDER BY ms.name;
