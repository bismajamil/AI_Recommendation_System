// Content-based recommendation engine
export function getRecommendations(userPreferences, allContent) {
  // Filter content that matches user preferences
  const scoredContent = allContent.map((item) => {
    // Count how many user preferences match with item categories
    const matchCount = userPreferences.filter((pref) =>
      item.categories.includes(pref.toLowerCase())
    ).length;

    // Calculate score based on matches and rating
    const score = matchCount > 0 ? matchCount * item.rating : 0;

    return {
      ...item,
      matchScore: score,
      matchCount: matchCount,
    };
  });

  // Filter out items with no matches and sort by score
  const recommendations = scoredContent
    .filter((item) => item.matchScore > 0)
    .sort((a, b) => b.matchScore - a.matchScore);

  return recommendations;
}
