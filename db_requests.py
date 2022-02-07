GET_SEARCH_RESULT_REQ = '''
SELECT id, sex, name, age, sex_partner, age_partner_from, age_partner_to, meeting_id FROM users 
WHERE sex = ? AND age >= ? AND age < ? AND id != ? LIMIT 10  
'''

GET_ALTER_SEARCH_RESULT_REQ = '''
SELECT id, sex, name, age, sex_partner, age_partner_from, age_partner_to, meeting_id FROM users 
WHERE id != ? LIMIT 10  
'''

REG_NEW_USER_REQ = '''
INSERT INTO users(id, sex, name, age, sex_partner, age_partner_from, age_partner_to) VALUES (?,?,?,?,?,?,?)
'''

ADD_PARTNER_REQ = '''
UPDATE users SET meeting_id = ? WHERE id = ?
'''